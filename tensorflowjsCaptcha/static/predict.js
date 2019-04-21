$("#image-selector").change(function () {
    let reader = new FileReader();
    reader.onload = function () {
        let dataURL = reader.result;
        $("#selected-image").attr("src", dataURL);
        $("#prediction-list").empty();
    }
    let file = $("#image-selector").prop("files")[0];
    reader.readAsDataURL(file);
}); 

let model;
(async function () {
    model = await tf.loadLayersModel('http://127.0.0.1:8008/tfjsmodel/model.json');
    $(".progress-bar").hide();
})();

$("#predict-button").click(async function () {
    let image = $("#selected-image").get(0);

    let tensor = tf.browser.fromPixels(image).toFloat();

    let offset = tf.scalar(127.5);
    tensor = tensor.sub(offset).div(offset).expandDims();


    console.log(tensor.shape);
    
    let predictions = await model.predict(tensor);
    let predict_charOne = await predictions[0].argMax(-1).data();
    var predictedCaptcha= String.fromCharCode(97 + predict_charOne[0]);
    
    let predict_charTwo = await predictions[1].argMax(-1).data();
    predictedCaptcha += String.fromCharCode(97 + predict_charTwo[0]);

    let predict_charThree = await predictions[2].argMax(-1).data();
    predictedCaptcha += String.fromCharCode(97 + predict_charThree[0]);

    let predict_charFour = await predictions[3].argMax(-1).data();
    predictedCaptcha += String.fromCharCode(97 + predict_charFour[0]);

    let predict_charFive = await predictions[4].argMax(-1).data();
    predictedCaptcha += String.fromCharCode(97 + predict_charFive[0]);

    let predict_charSix = await predictions[5].argMax(-1).data();
    predictedCaptcha += String.fromCharCode(97 + predict_charSix[0]);

    console.log(predictedCaptcha)

    document.getElementById("predictedCaptcha").innerHTML = predictedCaptcha;

    
    
})