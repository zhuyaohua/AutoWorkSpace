function onmessage(e) {
    let blob = new Blob([e.data])
    // 获取当前类型
    let reader = new FileReader()
    // 心跳检测
    this.heartCheckBack = true
    this.handleStartHeartCheck()
    reader.addEventListener('loadend', (e) => {
        let dataView = new DataView(reader.result)
        if (!dataView.byteLength || dataView.byteLength === 4) {
            return false
        }
        let number = dataView.getInt32(0, true)
        let length = dataView.getInt32(4, true)
        let json = reader.result.slice(8, 12)
        let sign = String.fromCharCode.apply(null, new Uint8Array(json))
        // console.log(length, number, json, sign, '---------------------->>>返回序号')
        if (sign === 'json') {
            this.responseNumber = number
            try {
                let jsonArr = []
                let constNum = 15000
                let num = Math.ceil((length - 12) / constNum)
                for (let n = 1; n <= num; n++) {
                    let start = n === 1 ? 12 : (n - 1) * constNum
                    let end = n === num ? length + 8 : n * constNum
                    let s = reader.result.slice(start, end)
                    let str = String.fromCharCode.apply(null, new Uint8Array(s))
                    jsonArr.push(str)
                }
                let jsonStr = jsonArr.join('')
                // console.log(jsonStr)
                // let jsonStr = String.fromCharCode.apply(null, new Uint8Array(reader.result.slice(12, length)))
                if (/^%/.test(jsonStr)) {
                    jsonStr = decodeURIComponent(jsonStr)
                }
                let dataVal = jsonStr && JSON.parse(jsonStr) || {}

                dataVal.number = number
                dataVal.canvasInfo = {
                    offsetX: this.canvas.offsetX,
                    offsetY: this.canvas.offsetY,
                    performance: this.performance,
                    realWidth: this.canvas.realWidth,
                    realHeight: this.canvas.realHeight,
                }
                this.handleGraphicJsonReply(dataVal)
                let imgBlob = blob.slice(8 + length)
                let imgUrl
                if (imgBlob.size) {
                    imgUrl = URL.createObjectURL(imgBlob)
                }
                this.drawImage(imgUrl, this.responseNumber)
                return false
            } catch (e) {
                console.warn('Invalid Data', e)
            }
        } else if (length === -520103681) {
            this.responseNumber = number
            let imgUrl = URL.createObjectURL(blob.slice(4))
            this.drawImage(imgUrl, this.responseNumber)
        }
    })
    reader.readAsArrayBuffer(blob)
}

onmessage({data:1})