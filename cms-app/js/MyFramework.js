class MyFramework {
    /**
     * getElementById: Busca un elemento del DOM por su ID
     * @param id : String con el id a buscar
     * @returns : Objeto HTMLElement encontrado
     */
    getElementById(id) {
        let el;
        el = document.getElementById(id);
        return el;
    }
    /**
     * getElementByEvent: Busca un elemento del DOM por el evento generado
     * @param evt: Objeto evento generado
     * @returns : Objeto HTMLElement encontrado
     */
    getElementByEvent(evt) {
        return evt.target;
    }
    /**
     * configClick: Agrega a un determinado elemento del HTML (identificado por su id) un listener
     * de evento a la espera de un click
     * @param id el id del HTMLElement
     * @param listener el listener del evento
     */
    configClick(id, listener) {
        let b = this.getElementById(id);
        b.addEventListener("click", listener);
    }
    /**
     * requestGET Ejecuta un request GET al generarse un determinado evento por un objeto
     * @param url: String de una URL a la cual queremos realizar el request GET
     * @param listener: Listener para detectar un evento
     * @returns : Void ()
     */
    requestGET(url, listener) {
        let xhr;
        xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    listener.handleGETResponse(xhr.status, xhr.responseText);
                }
                else {
                    listener.handleGETResponse(xhr.status, null);
                }
            }
        };
        xhr.open('GET', url, true);
        xhr.send(null);
    }
    /**
     * requestPOST Ejecuta un request POST al generarse un determinado evento por un objeto
     * @param url: String de una URL a la cual queremos realizar el request POST
     * @param listener: Listener para detectar un evento
     * @returns : Void ()
     */
    requestPOST(url, data, listener) {
        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    listener.handlePOSTResponse(xhr.status, xhr.responseText);
                }
                else {
                    listener.handlePOSTResponse(xhr.status, null);
                }
            }
        };
        xhr.open("POST", url);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify(data));
    }
}
