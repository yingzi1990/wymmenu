import { api } from "../../scripts/api.js";
import { app } from "../../scripts/app.js";
import { $el } from "../../scripts/ui.js";

const style = `
#comfy-floating-button {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: auto;
    height: 50px;
    border-radius: 10px;
    background-color: rgb(130, 88, 245);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.25);
    user-select: none;
    padding: 0 15px;
    white-space: nowrap;
}

#comfy-floating-button:hover {
    background-color: rgb(100, 68, 215);
}

.comfy-floating-menu .context-menu-item {
    position: relative;
}

.comfy-floating-menu .context-menu-item .summary {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    background: white;
    color: black;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    white-space: nowrap;
    z-index: 1000;
}

.comfy-floating-menu .context-menu-item:hover .summary {
    display: block;
}

#comfy-hide-button {
    position: absolute;
    top: 5px;
    left: 5px;
    cursor: pointer;
    color: white;
    font-size: 12px;
}
.example-menu {
    background-color: var(--comfy-menu-bg);
    filter: brightness(95%);
    will-change: transform;
    min-width: 100px;
    box-shadow: 0 0 10px black;
    padding: 10px;
    margin: 0;
}
.example-menu li {
    list-style: none;
    cursor: pointer;
    line-height: 1.5;
    padding: 0;
    margin: 4px 0;
    position: relative;
    padding-left: 20px;
}
.example-menu li.has-child::before {
    content: "▶";
    margin-right: 5px;
    transition: all 0.1s;
    position: absolute;
    left: 0;
    top: 0;
}
.example-menu li.has-child.show-child::before {
    transform: rotate(90deg);
}
.example-menu li .child-list {
    padding-left: 0px;
}
`;

class menuButton {
    constructor(menu) {
        this.menu = menu.menu
        this.button = $el("div", {
            id: "comfy-floating-button",
            textContent: "☁️"+menu.name+"➕",
            onmousedown: (e) => this.startDrag(e),
            onclick: (e) => this.showMenu(e),
        });
        this.hideButton = $el("div", {
            id: "comfy-hide-button",
            textContent: "✕",
            onclick: (e) => this.toggleVisibility(e),
        });
        this.button.appendChild(this.hideButton);
        document.body.appendChild(this.button);
        this.dragging = false;
        this.visible = true;

        document.addEventListener("mousemove", (e) => this.doDrag(e));
        document.addEventListener("mouseup", () => this.endDrag());
        document.addEventListener("click", () => {
            const exampleMenu = document.querySelector(".example-menu")
            if (exampleMenu) document.body.removeChild(exampleMenu);
        });
    }

    async showMenu(e) {
        if (this.dragging) return; // Prevent showing menu during drag
        e.preventDefault();
        e.stopPropagation();

        const exampleMenu = document.querySelector(".example-menu")
        if (exampleMenu) document.body.removeChild(exampleMenu);
        const keys = Object.keys(this.menu)
        document.body.appendChild($el(
            "ul.example-menu",
            {
                style: {
                    position: "absolute",
                    top: e.clientY + "px",
                    left: e.clientX + "px",
                    zIndex: 1000,
                }
            },
            keys.map(item => this.mapHtmls(this.menu[item], item))
        ))
    }

    mapHtmls(item, key) {
        if (typeof item === 'object') {
            const keys = Object.keys(item)
            return $el("li.has-child", {
                textContent: key,
                onclick: function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const childList = this.querySelector(".child-list");
                    this.classList.toggle('show-child');
                    childList.style.display = childList.style.display === 'block' ? 'none' : 'block';
                }
            }, [
                $el("ul.child-list", { style: { display: "none" } }, keys.map(e => this.mapHtmls(item[e], e)))
            ])
        } else {
            return $el("li", {
                textContent: key,
                onclick: async () => await this.get_workflow_graph(item)
            });
        }
    }

    async get_workflow_graph(file) {
        const exampleMenu = document.querySelector(".example-menu")
        if (exampleMenu) document.body.removeChild(exampleMenu);
        const response = await api.fetchApi("/wymcomfy/workflow", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ file: file }),
        });
        const showcase_graph = await response.json()
        console.log("showcase_graph:", showcase_graph);
        if (showcase_graph.error) {
            if (showcase_graph.error === "api error code:10001") {
                this.showInputDialog(file)
            }
        }else{
            app.graph.clear()
            await app.loadGraphData(showcase_graph)
        }
    }
    async showInputDialog(file) {
        // Create and show input dialog
        const input = $el("input", { type: "text", placeholder: "请输入密钥激活使用" });
        const confirmButton = $el("button", {textContent: "激活"});
        const dialog = $el("div", {
            style: {
                position: "fixed",
                top: "30%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                background: "white",
                padding: "20px",
                borderRadius: "5px",
                boxShadow: "0 0 10px rgba(0,0,0,0.2)",
                zIndex: "1001"
            }
        }, [
            input,
            confirmButton
        ]);
    
        document.body.appendChild(dialog);
    
        confirmButton.onclick = async () => {
            const value = input.value;
            if (value.trim() !== '') {
                const response = await api.fetchApi("/wymcomfy/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({secret: value}),
                });
                const result = await response.json();
                if(result.error){
                    alert(result.error);
                }else{
                    console.log("login success file:", file);
                    this.get_workflow_graph(file)
                    document.body.removeChild(dialog);
                }
            }
        };
    
        // Close dialog on click outside
        document.addEventListener('click', function onClickOutside(e) {
            if (!dialog.contains(e.target)) {
                document.body.removeChild(dialog);
                document.removeEventListener('click', onClickOutside);
            }
        });
    }
    async getMenuOptions() {
        return this.menu.map(item => ({
            title: item.title,
            callback: async () => await this.get_workflow_graph(item.file),
        }));
    }

    startDrag(e) {
        this.dragging = true;
        this.offsetX = e.clientX - this.button.offsetLeft;
        this.offsetY = e.clientY - this.button.offsetTop;
    }

    endDrag() {
        this.dragging = false;
    }

    doDrag(e) {
        if (this.dragging) {
            this.button.style.left = (e.clientX - this.offsetX) + 'px';
            this.button.style.top = (e.clientY - this.offsetY) + 'px';
            this.button.style.bottom = 'auto';
            this.button.style.right = 'auto';
        }
    }

    toggleVisibility(e) {
        e.stopPropagation();
        if (this.visible) {
            this.button.style.display = "none";
        } else {
            this.button.style.display = "flex";
        }
        this.visible = !this.visible;
    }
}

app.registerExtension({
    name: "wymcomfy.menuButton",
    async setup() {
        $el("style", {
            textContent: style,
            parent: document.head,
        });
        const response = await api.fetchApi("/wymcomfy/routesmenu",
            { method: "GET" });
        if (response.status === 200) {
            const menu = await response.json()
            console.log('http',menu);
            new menuButton(menu);
        } else {
            console.log("error occurs when fetch the showcases:", await response.text())
        }
    },
});
