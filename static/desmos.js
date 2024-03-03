var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);
var imageCount = 4;


function setBounds() {
    // calculator.setMathBounds({ 
    //     left: -221.17,
    //     right: 1450.084, 
    //     bottom: -155.929, 
    //     top: 1081.27
    //   });
    calculator.setMathBounds({  // -188.253, 780.208, -45.518, 671.416
        left: -188.253,
        right: 780.208,
        bottom: -45.518,
        top: 671.416
      });
}

setBounds();
var defaultState = calculator.getState();
var pass = 0;
var imageChunks = 4;
var totalTime = 0;


async function drawLines(lines) {
    return new Promise(async resolve => {
        var startTime = performance.now()
        var color = '#000000';

        var start = pass * Math.floor(lines.length / imageChunks);
        var end = (pass + 1) * Math.floor(lines.length / imageChunks);

        for (var i = start; i < end; i++) {
            if (lines[i].startsWith('#')) {
                color = lines[i];
            } else {
                calculator.setExpression({ color: color, latex: lines[i] });
            }
        }
    
        pass++;

        const elapsedTime = performance.now() - startTime;
        // console.log("Time: " + elapsedTime);
        totalTime += elapsedTime;

        await takeScreenshot();
        resolve();
    });
    
}


async function takeScreenshot() {
    return new Promise(async resolve => {
        var opts = {
            "mode": "contain",
            "width": window.screen.width,
            "height": window.screen.height,
            "targetPixelRatio": 1,
            "preserveAxisNumers": false
        };
    
        calculator.asyncScreenshot(opts, downloadImage);
        await removeLines();
        resolve();
    })
}


async function downloadImage(imageData) {
    var img = document.createElement('a');
    img.style.display = 'none';
    
    img.href = imageData;

    img.download = "rick_" + imageCount + '.png';
    imageCount++;

    document.body.appendChild(img);

    img.click();

    document.body.removeChild(img);    
}

async function removeLines() {
    calculator.setState(defaultState);
}


async function processEquations() {
    const chunkSize = 10;
    const totalChunks = Math.ceil(equations.length / chunkSize);

    for (var i = 0; i < totalChunks; i++) {
        const start = chunkSize * i;
        const end = Math.min(start + chunkSize, equations.length);
        const chunk = equations.slice(start, end);

        await processChunk(chunk);
    }
}

async function processChunk(chunk) {
    for (const equations of chunk) {
        await drawLines(equations);
        if (pass > imageChunks - 1) {
            pass = 0;
            console.log("Total Time: " + totalTime);
        }
    }
}


for (var i = 0; i < imageChunks; i++) {
    processEquations();
}



