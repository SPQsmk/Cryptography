let apiTask
let mode = "cbc"
let size = "16"

function get_mode() {
    let target = event.target

    mode = target.value
}

function get_block_size() {
    let target = event.target

    size = target.value
}

function choose_message() {
    const file = document.getElementById("file")
    const txt = document.getElementById("file__name")

    file.click()

    file.addEventListener("change", function () {
        let fullpath = file.value
        if (fullpath) {
            let startIndex = (fullpath.indexOf("\\") >= 0 ? fullpath.lastIndexOf("\\") : fullpath.lastIndexOf("/"))
            let filename = fullpath.substring(startIndex)
            if (filename.indexOf("\\" === 0) || filename.indexOf("/") === 0) {
                filename = filename.substring(1)
            }
            if (filename.length < 20) {
                txt.innerHTML = filename
            } else {
                txt.innerHTML = filename.substring(0, 20) + "..."
            }
        } else {
            txt.innerHTML = "Выберите файл"
        }
    })
}

function choose_key() {
    const file = document.getElementById("key")
    const key = document.getElementById("key__name")

    file.click()

    file.addEventListener("change", function () {
        let fullpath = file.value
        if (fullpath) {
            let startIndex = (fullpath.indexOf("\\") >= 0 ? fullpath.lastIndexOf("\\") : fullpath.lastIndexOf("/"))
            let filename = fullpath.substring(startIndex)
            if (filename.indexOf("\\" === 0) || filename.indexOf("/") === 0) {
                filename = filename.substring(1)
            }
            if (filename.length < 20) {
                key.innerHTML = filename
            } else {
                key.innerHTML = filename.substring(0, 20) + "..."
            }
        } else {
            key.innerHTML = "Выберите файл"
        }
    })
}

function communicate() {
    let xhr = new XMLHttpRequest();
    let res = document.getElementById("res")
    let json
    let form

    res.innerHTML = "Ожидайте..."

    switch(apiTask) {
        case "getbit":
        case "changebit":
        case "zerobits":
        case "gluebits":
        case "midbits":
        case "leftshift":
        case "rightshift":
        case "transposebits":
        case "euclid":
        case "exeuclid":
        case "gfmul":
            json = JSON.stringify({
                a: document.getElementById("a").value,
                k: document.getElementById("k").value
            })
            break
        case "swapbits":
        case "swapbytes":
        case "fastpow":
            json = JSON.stringify({
                a: document.getElementById("a").value,
                i: document.getElementById("i").value,
                j: document.getElementById("j").value
            })
            break
        case "maxpow2":
        case "withinrange":
        case "xorall":
        case "gfpolinom":
        case "gfinv":
        case "euler":
            json = JSON.stringify({
                x: document.getElementById("x").value
            })
            break
        case "vernam":
            form = new FormData();
            message = document.getElementById("file")
            key = document.getElementById("key")
            if (!key.value || !message.value) {
                res.innerHTML = ""
                return
            }
            form.append("file", message.files[0])
            form.append("key", key.files[0])
            break
        case "des":
            form = new FormData();
            message = document.getElementById("file")
            if (!message.value) {
                res.innerHTML = ""
                return
            }
            form.append("file", message.files[0])
            form.append("key", document.getElementById("key").value)
            form.append("c0", document.getElementById("c0").value)
            form.append("mode", mode)
            form.append("decode", document.getElementById("checkbox").checked)
            break
        case "rc4":
            form = new FormData();
            message = document.getElementById("file")
            if (!message.value) {
                res.innerHTML = ""
                return
            }
            form.append("file", message.files[0])
            form.append("key", document.getElementById("key"))
            break
        case "rsa":
            form = new FormData();
            message = document.getElementById("file")
            key = document.getElementById("key")
            decode = !key.value ? false : true
            if (!message.value) {
                res.innerHTML = ""
                return
            }
            if (key.value) {
                form.append("key", key.files[0])
            } 
            form.append("decode", decode)
            form.append("file", message.files[0])
            xhr.open("POST", "http://127.0.0.1:5000/" + apiTask)
            xhr.send(form)
            xhr.onerror = function() {
                res.innerHTML = "Не удаляй файл"
            }
            xhr.onload = function () {
                js = JSON.parse(xhr.response)
                if (js["path"] == undefined) {
                    res.innerHTML = js["error"]
                } else if (!decode) {
                    res.innerHTML = `<a class="file__link" href="${js["path"]}">Скачать файл</a>
                                    <br>
                                    <a class="file__link" href="${js["key"]}">Скачать ключ</a>`
                } else {
                    res.innerHTML = `<a class="file__link" href="${js["path"]}">Скачать файл</a>`
                }
            }
            return
        case "rds":
        case "factorization":
        case "simplenums":
            json = JSON.stringify({
                m: document.getElementById("m").value
            })
            xhr.open("POST", "http://127.0.0.1:5000/" + apiTask)
            xhr.setRequestHeader("Content-type", "application/json")
            xhr.send(json)
            xhr.onerror = function() {
                res.innerHTML = "Не удаляй файл"
            }
            xhr.onload = function () {
                js = JSON.parse(xhr.response)
                if (js["path"] == undefined) {
                    res.innerHTML = js["error"]
                } else {
                    res.innerHTML = `<a class="file__link" href="${js["path"]}">Скачать</a>`
                }
            }
            return
        case "rijndael":
            form = new FormData();
            message = document.getElementById("file")
            if (!message.value) {
                res.innerHTML = ""
                return
            }
            form.append("file", message.files[0])
            form.append("key", document.getElementById("key").value)
            form.append("c0", document.getElementById("c0").value)
            form.append("block_size", size)
            form.append("mode", mode)
            form.append("decode", document.getElementById("checkbox").checked)
            break
    }

    xhr.open("POST", "http://127.0.0.1:5000/" + apiTask)
    if (apiTask === "rc4" || apiTask === "des" || apiTask === "vernam" || apiTask === "rijndael") {
        xhr.send(form)
        xhr.onerror = function() {
            res.innerHTML = "Не удаляй файл"
        }
        xhr.onload = function () {
            js = JSON.parse(xhr.response)
            if (js["path"] == undefined) {
                res.innerHTML = js["error"]
            } else {
                res.innerHTML = `<a class="file__link" href="${js["path"]}">Скачать</a>`
            }
        }
    } else {
        xhr.setRequestHeader("Content-type", "application/json")
        xhr.send(json)
        xhr.onerror = function() {
            res.innerHTML = "Не удаляй файл"
        }
        xhr.onload = function () {
            js = JSON.parse(xhr.response)
            if (js["res"] == undefined) {
                res.innerHTML = js["error"]
            } else {
                res.innerHTML = js["res"]
            }
        }
    }
}

function task() {
    let target = event.target
    let value = target.value
    let form = document.getElementById("form__inner")
    let slider = document.getElementById("slider__inner")

    switch(value) {
        case "11A":
            apiTask = "getbit"
            form.innerHTML = `
                <div class="form__title">Получить k-ый бит числа a</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1.1</div>`
            break
        case "11B":
            apiTask = "changebit"
            form.innerHTML = `
                <div class="form__title">Заменить k-ый бит числа a</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1.2</div>`
            break
        case "11C":
            apiTask = "swapbits"
            form.innerHTML = `
                <div class="form__title">Поменять i и j биты местами</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="i">
                    <label class="form__label">i</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="j">
                    <label class="form__label">j</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1.3</div>`
            break
        case "11D":
            apiTask = "zerobits"
            form.innerHTML = `
                <div class="form__title">Обнулить младшие k бит</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1.4</div>`
            break
        case "12A":
            apiTask = "gluebits"
            form.innerHTML = `
                <div class="form__title">Склеить первые и последние k бит</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 2.1</div>`
            break
        case "12B":
            apiTask = "midbits"
            form.innerHTML = `
                <div class="form__title">Получить средние (len - 2k) бит</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 2.2</div>`
            break
        case "13":
            apiTask = "swapbytes"
            form.innerHTML = `
                <div class="form__title">Поменять i и j байты местами</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="i">
                    <label class="form__label">i</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="j">
                    <label class="form__label">j</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 3</div>`
            break
        case "14":
            apiTask = "maxpow2"
            form.innerHTML = `
                <div class="form__title">Максимальная степень 2, на которую делится число x</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 4</div>`
            break
        case "15":
            apiTask = "withinrange"
            form.innerHTML = `
                <div class="form__title">Найти p: 2^p < x < 2^(p+1)</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 5</div>`
            break
        case "16":
            apiTask = "xorall"
            form.innerHTML = `
                <div class="form__title">XOR всех битов числа x</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 6</div>`
            break
        case "17A":
            apiTask = "leftshift"
            form.innerHTML = `
                <div class="form__title">Циклический сдвиг влево на k бит</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 7.1</div>`
            break
        case "17B":
            apiTask = "rightshift"
            form.innerHTML = `
                <div class="form__title">Циклический сдвиг вправо на k бит</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 7.2</div>`
            break
        case "18":
            apiTask = "transposebits"
            form.innerHTML = `
                <div class="form__title">Перестановка бит в числе a</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k (1,5,7,...)</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 8</div>`
            break
        case "19":
            apiTask = "vernam"
            form.innerHTML = `
                <div class="form__title">Шифр Вернама</div>
                <input type="file" id="file" hidden="hidden">
                <div class="file__input" onclick="choose_message()">message</div>
                <span id="file__name" class="file__name">Выберите файл</span>
                <br>
                <input type="file" id="key" hidden="hidden">
                <div class="file__input" onclick="choose_key()">key</div>
                <span id="key__name" class="file__name">Выберите файл</span>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 9</div>`
            break
        case "110":
            apiTask = "des"
            form.innerHTML = `
                <div class="form__title">Шифр DES</div>
                <input type="file" id="file" hidden="hidden">
                <div class="file__input" onclick="choose_message()">message</div>
                <span id="file__name" class="file__name">Выберите файл</span>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="key">
                    <label class="form__label">key (8 bytes)</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="c0">
                    <label class="form__label">c0 (8 bytes)</label>
                </div>
                <div class="mode__container" onclick="get_mode()">
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="cbc" value="cbc" checked>
                        <label class="mode__label" for="cbc">CBC</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="ecb" value="ecb">
                        <label class="mode__label" for="ecb">ECB</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="cfb" value="cfb">
                        <label class="mode__label" for="cfb">CFB</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="ofb" value="ofb">
                        <label class="mode__label" for="ofb">OFB</label>
                    </div>
                </div>
                <div class="checkbox">
                    <input type="checkbox" class="checkbox__input" id="checkbox">
                    <label for="checkbox" class="checkbox__label">Decode</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 10</div>`
            break
        case "111":
            apiTask = "rc4"
            form.innerHTML = `
                <div class="form__title">Шифр RC4</div>
                <input type="file" id="file" hidden="hidden">
                <div class="file__input" onclick="choose_message()">message</div>
                <span id="file__name" class="file__name">Выберите файл</span>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="key">
                    <label class="form__label">key</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 11</div>`
            break
        case "21":
            apiTask = "simplenums"
            form.innerHTML = `
                <div class="form__title">Вывести простые числа меньше m</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="m">
                    <label class="form__label">m</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1</div>`
            break
        case "22":
            apiTask = "rds"
            form.innerHTML = `
                <div class="form__title">Вывести приведенную систему вычетов по модулю m</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="m">
                    <label class="form__label">m</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 2</div>`
            break
        case "23":
            apiTask = "euler"
            form.innerHTML = `
                <div class="form__title">Функция Эйлера от x</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 3</div>`
            break
        case "24":
            apiTask = "factorization"
            form.innerHTML = `
                <div class="form__title">Каноническое разложение числа m по степеням простых чисел</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="m">
                    <label class="form__label">m</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 4</div>`
            break
        case "25":
            apiTask = "fastpow"
            form.innerHTML = `
                <div class="form__title">Быстрое возведение числа a в степень i по модулю j</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="i">
                    <label class="form__label">i</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="j">
                    <label class="form__label">j</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 5</div>`
            break
        case "26":
            apiTask = "euclid"
            form.innerHTML = `
                <div class="form__title">Алгоритм Евклида</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 6</div>`
            break
        case "27":
            apiTask = "exeuclid"
            form.innerHTML = `
                <div class="form__title">Расширенный алгоритм Евклида</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 7</div>`
            break
        case "28":
            apiTask = "rsa"
            form.innerHTML = `
                <div class="form__title">Шифр RSA</div>
                <input type="file" id="file" hidden="hidden">
                <div class="file__input" onclick="choose_message()">message</div>
                <span id="file__name" class="file__name">Выберите файл</span>
                <br>
                <input type="file" id="key" hidden="hidden">
                <div class="file__input" onclick="choose_key()">key</div>
                <span id="key__name" class="file__name">Выберите файл</span>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 8</div>`
            break
        case "31":
            apiTask = "gfpolinom"
            form.innerHTML = `
                <div class="form__title">Полиномиальная форма для GF(256)</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 1</div>`
            break
        case "32":
            apiTask = "gfmul"
            form.innerHTML = `
                <div class="form__title">Умножение полиномов a и k из GF(256)</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="a">
                    <label class="form__label">a</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="k">
                    <label class="form__label">k</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 2</div>`
            break
        case "33":
            apiTask = "gfinv"
            form.innerHTML = `
                <div class="form__title">Обратное для x из GF(256)</div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="x">
                    <label class="form__label">x</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 3</div>`
            break
        case "34":
            apiTask = "rijndael"
            form.innerHTML = `
                <div class="form__title">Шифр Rijndael</div>
                <input type="file" id="file" hidden="hidden">
                <div class="file__input" onclick="choose_message()">message</div>
                <span id="file__name" class="file__name">Выберите файл</span>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="key">
                    <label class="form__label">key (16/24/32 bytes)</label>
                </div>
                <div class="form__group">
                    <input class="form__input" placeholder=" " id="c0">
                    <label class="form__label">c0 (equal to block size)</label>
                </div>
                <div class="block__container" onclick="get_block_size()">
                    Размер блока:
                    <div class="block">
                        <input class="block__radio" name="block_size" type="radio" id="16" value="16" checked>
                        <label class="block__label" for="16">16</label>
                    </div>
                    <div class="block">
                        <input class="block__radio" name="block_size" type="radio" id="24" value="24">
                        <label class="block__label" for="24">24</label>
                    </div>
                    <div class="block">
                        <input class="block__radio" name="block_size" type="radio" id="32" value="32">
                        <label class="block__label" for="32">32</label>
                    </div>
                </div>
                <div class="mode__container" onclick="get_mode()">
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="cbc" value="cbc" checked>
                        <label class="mode__label" for="cbc">CBC</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="ecb" value="ecb">
                        <label class="mode__label" for="ecb">ECB</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="cfb" value="cfb">
                        <label class="mode__label" for="cfb">CFB</label>
                    </div>
                    <div class="mode">
                        <input class="mode__radio" name="mode" type="radio" id="ofb" value="ofb">
                        <label class="mode__label" for="ofb">OFB</label>
                    </div>
                </div>
                <div class="checkbox">
                    <input type="checkbox" class="checkbox__input" id="checkbox">
                    <label for="checkbox" class="checkbox__label">Decode</label>
                </div>
                <button type="submit" class="btn" onclick="communicate()">Отправить</button>
                <div class="form__result" id="res"></div>`
            slider.innerHTML = `<div class="slider__item"># 4</div>`
            break
    }
}

lab__nav.onclick = task