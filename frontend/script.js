console.log("SCRIPT IS WORKING");

const fileInput = document.getElementById("fileInput");
const detectButton = document.getElementById("detectButton");
const resultDiv = document.getElementById("result");

detectButton.addEventListener("click", async function () {

    console.log("BUTTON CLICKED");

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image or video.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    resultDiv.innerHTML = `
        <p>Detecting...</p>
    `;

    try {

        // Check whether file is image or video
        const isVideo = file.type.startsWith("video/");

        let endpoint;

        if (isVideo) {
            endpoint = "http://127.0.0.1:8000/detect-video";
        } else {
            endpoint = "http://127.0.0.1:8000/detect";
        }

        console.log("Sending to:", endpoint);

        const response = await fetch(endpoint, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const result = await response.json();

        console.log(result);

        const human =
            Number(result.probabilities.human);

        const artificial =
            Number(result.probabilities.artificial);

        let prediction;
        let confidence;

        if (artificial > human) {

            prediction = isVideo
                ? "AI GENERATED VIDEO"
                : "AI GENERATED";

            confidence = artificial;

        } else {

            prediction = isVideo
                ? "REAL / HUMAN VIDEO"
                : "REAL / HUMAN";

            confidence = human;
        }

        resultDiv.innerHTML = `

            <h2>${prediction}</h2>

            <p>
                File: ${result.filename}
            </p>

            <p>
                Confidence:
                <strong>
                    ${confidence.toFixed(2)}%
                </strong>
            </p>

            <p>
                Human:
                ${human.toFixed(2)}%
            </p>

            <p>
                Artificial:
                ${artificial.toFixed(2)}%
            </p>

        `;

    } catch (error) {

        console.error(error);

        resultDiv.innerHTML = `
            <p>
                Detection failed.
            </p>
        `;
    }

});