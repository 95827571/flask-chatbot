const messageHolder = document.getElementById("message-holder")

const createDiv = (messageDetails, index, timeBetweenLetter=100) => {
    const msgDiv = document.createElement("div")
    msgDiv.classList.add("msg-wrapper", messageDetails.user == "Bot" ? "bot-m-wrapper" : "user-m-wrapper")

    const usernameP = document.createElement("p")
    usernameP.innerText = messageDetails.user
    usernameP.classList.add("message-user-title")
    msgDiv.appendChild(usernameP)

    const msgBoxDiv = document.createElement("div")
    msgBoxDiv.classList.add("message", messageDetails.user == "Bot" ? "bot-msg" : "user-msg")
    msgDiv.appendChild(msgBoxDiv)

    const messageP = document.createElement("p")
    messageP.classList.add("message-text")
    msgBoxDiv.appendChild(messageP)
    
    
    messageHolder.appendChild(msgDiv)
    let lastChar = 0
    const typewriter = () => {
        setTimeout(() => {
            if (lastChar == messageDetails.message.length) {
                return;
            }
            messageP.textContent += messageDetails.message[lastChar]
    
            lastChar++;
            typewriter();
        }, timeBetweenLetter)
    }
    typewriter()
    messageHolder.scrollTo(0, messageHolder.scrollHeight)
}