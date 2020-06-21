class ViewMainPage {
    constructor(myf) {
        this.myf = myf;
    }
    showDevices(list) {
        // cargo la lista de objetos en el DOM
        let devicesUl = this.myf.getElementById("devicesList");
        let items = "";
        for (let i in list) {
            let checkedStr = "";
            if (list[i].state == "1")
                checkedStr = "checked";
            switch (list[i].type) {
                case 0: // Lampara                     
                    items += "<li class='collection-item avatar'> \
                                <img src='images/lightbulb.png' alt='' class='circle'> \
                                <span class='title'>" + list[i].name + "</span> \
                                <p>" + list[i].description + "<br> \
                                </p> \
                                <a href='#!' class='secondary-content'> <div class='switch'> \
                                                                            <label> \
                                                                            Off \
                                                                            <input type='checkbox' id='dev_" + list[i].id + "' " + checkedStr + "> \
                                                                            <span class='lever'></span> \
                                                                            On \
                                                                            </label> \
                                                                        </div></a> \
                            </li>";
                    break;
                case 1: // Persiana                    
                    items += "<li class='collection-item avatar'> \
                                <img src='images/window.png' alt='' class='circle'> \
                                <span class='title'>" + list[i].name + "</span> \
                                <p>" + list[i].description + "<br> \
                                </p> \
                                <a href='#!' class='secondary-content'> <div class='switch'> \
                                                                            <label> \
                                                                            Off \
                                                                            <input type='checkbox' id='dev_" + list[i].id + "' " + checkedStr + "> \
                                                                            <span class='lever'></span> \
                                                                            On \
                                                                            </label> \
                                                                        </div></a> \
                            </li>";
                    break;
            }
        }
        devicesUl.innerHTML = items;
    }
    getSwitchStateById(id) {
        let el = this.myf.getElementById(id);
        return el.checked;
    }
}
class Main {
    handleEvent(evt) {
        let sw = this.myf.getElementByEvent(evt);
        //Defino e inicializo las URLs para realizar los requests GET al filtrar dispositivos
        let urlFiltradotodos = 'ws/devices?filter=0';
        let urlFiltradoLamparas = 'ws/devices?filter=1';
        let urlFiltradoPersianas = 'ws/devices?filter=2';
        if (sw.id === "botonTodos") {
            console.log("Mostrando todos los dispositivos...");
            this.myf.requestGET(urlFiltradotodos, this);
        }
        else if (sw.id === "botonLamparas") {
            console.log("Mostrando solo las lamparas...");
            this.myf.requestGET(urlFiltradoLamparas, this);
        }
        else if (sw.id === "botonPersianas") {
            console.log("Mostrando solo las persianas...");
            this.myf.requestGET(urlFiltradoPersianas, this);
        }
        else {
            let data = { "id": sw.id, "state": this.view.getSwitchStateById(sw.id) };
            this.myf.requestPOST("devices", data, this);
        }
    }
    handleGETResponse(status, response) {
        if (status == 200) {
            console.log(response);
            let data = JSON.parse(response);
            console.log(data);
            this.view.showDevices(data);
            for (let i in data) {
                let sw = this.myf.getElementById("dev_" + data[i].id);
                sw.addEventListener("click", this);
            }
        }
    }
    handlePOSTResponse(status, response) {
        if (status == 200) {
            console.log(response);
        }
    }
    /**
     * agregarConfigClick Pasa cada string del array de IDs de elementos HTML como parametro para el
     * metodo configClick de MyFramework.ts
     * @param arr_ids array con strings de ids de los elementos HTML
     */
    agregarConfigClick(arr_ids) {
        for (let IdElemento of arr_ids) {
            this.myf.configClick(IdElemento, this);
        }
    }
    main() {
        this.myf = new MyFramework();
        this.view = new ViewMainPage(this.myf);
        this.myf.requestGET("devices", this);
        //Declaro e inicializo un array con los ids de los botones utilizados para filtrar
        let arrayIdElementos;
        arrayIdElementos = ["botonTodos", "botonLamparas", "botonPersianas"];
        this.agregarConfigClick(arrayIdElementos);
    }
}
window.onload = () => {
    let obj = new Main();
    obj.main();
};
