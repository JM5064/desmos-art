var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);
var count = 160;


function setBounds() {
    calculator.setMathBounds({ 
        left: -221.17,
        right: 1450.084, 
        bottom: -155.929, 
        top: 1081.27
      });
}

setBounds();
var defaultState = calculator.getState();
var pass = 0;
var imageChunks = 8;
var totalTime = 0;


async function drawLines(lines) {
    return new Promise(async resolve => {
        var startTime = performance.now()
        console.time();
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

        console.timeEnd();
        const elapsedTime = performance.now() - startTime;
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

    img.download = "rick_" + count + '.png';
    count++;

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

    for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
        const start = chunkIndex * chunkSize;
        const end = Math.min(start + chunkSize, equations.length);
        const chunk = equations.slice(start, end);

        await processChunk(chunk);
    }
}

async function processChunk(chunk) {
    for (const equation of chunk) {
        await drawLines(equation);
    }
}


for (var i = 0; i < imageChunks; i++) {
    processEquations();
}

console.log("Total Time " + totalTime);





