let elt = document.getElementById('calculator');
let calculator = Desmos.GraphingCalculator(elt);
let imageCount = 451;


function setBounds() {
    calculator.setMathBounds({ 
        left: -439.416,
        right: 1565.192, 
        bottom: -189.575, 
        top: 1294.4
      });
}

setBounds();
let defaultState = calculator.getState();
let pass = 0;
let imageChunks = 4;
let totalTime = 0;


async function drawLines(lines) {
    let startTime = performance.now()
    let color = '#000000';

    let start = pass * Math.floor(lines.length / imageChunks);
    let end = (pass + 1) * Math.floor(lines.length / imageChunks);

    for (let i = start; i < end; i++) {
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
}


async function takeScreenshot() {
    let opts = {
        "mode": "contain",
        "width": window.screen.width,
        "height": window.screen.height,
        "targetPixelRatio": 2,
        "preserveAxisNumers": false
    };

    calculator.asyncScreenshot(opts, downloadImage);
    await removeLines();
}


async function downloadImage(imageData) {
    let img = document.createElement('a');
    img.style.display = 'none';
    
    img.href = imageData;

    img.download = "LHpizz_" + imageCount + '.png';
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

    for (let i = 0; i < totalChunks; i++) {
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


for (let i = 0; i < imageChunks; i++) {
    processEquations();
}

