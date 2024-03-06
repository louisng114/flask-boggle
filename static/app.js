ansForm = document.querySelector("#ansForm");
ansInput = document.querySelector("#ans");
result = document.querySelector("#result");
scoreText = document.querySelector("#score");
timerText = document.querySelector("#timer");

let score = 0;
let timer = 60;

const ansHandler = async (evt) => {
    evt.preventDefault();
    ans = ansInput.value;
    check = await axios.post("/check", {
        "ans" :  ans
    });
    report = check.data["result"];
    result.innerText = report;
    if (report == "ok") {
        score += ans.length
        scoreText.innerText = "Score: " + score;
    }
    ansInput.value = "";
};

const countdown = () => {
    if (timer > 0) {
        timer--;
        timerText.innerText = "Time: " + timer;
    } else {
        timerText.innerText = "Time: 0";
        ansForm.remove();
        clearInterval(timerInterval);
        postScore();
    }
}

const postScore = async () => {
    await axios.post("/result", {
        "score" : score
    });
}

ansForm.addEventListener("submit", ansHandler);
const timerInterval = setInterval(countdown,1000);
