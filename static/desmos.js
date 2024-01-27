var elt = document.getElementById('calculator');
var calculator = Desmos.GraphingCalculator(elt);



function setBounds() {
    calculator.setMathBounds({
        left: -75.065,
        right: 1405.354,
        bottom: -161.045,
        top: 934.883
      });
}

setBounds();
var defaultState = calculator.getState();


async function drawLines(lines) {
    return new Promise(async resolve => {    
        var color = '#000000';
    
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith('#')) {
                color = lines[i];
            } else {
                calculator.setExpression({ color: color, latex: lines[i] });
            }
        }
    
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

    img.download = 'image5.jpg';

    document.body.appendChild(img);

    img.click();

    document.body.removeChild(img);    
}

async function removeLines() {
    calculator.setState(defaultState);
}


// async function processEquations() {
//     for (var img = 0; img < equations.length; img++) {
//         await drawLines(equations[img]);
//     }
// }
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



processEquations();

console.log("done");





