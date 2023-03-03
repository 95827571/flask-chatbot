const messageHolder = document.getElementById("message-holder")

const createDiv = (messageDetails, index, responseLength,  timeBetweenLetter=100) => {
    // Creates the wrapper for picking side
    const msgDiv = document.createElement("div")
    msgDiv.classList.add("msg-wrapper", messageDetails.user == "Bot" ? "bot-m-wrapper" : "user-m-wrapper")

    // Creates the user title text
    const usernameP = document.createElement("p")
    usernameP.innerText = messageDetails.user
    usernameP.classList.add("message-user-title")
    msgDiv.appendChild(usernameP)

    // Creates the message container
    const msgBoxDiv = document.createElement("div")
    msgBoxDiv.classList.add("message", messageDetails.user == "Bot" ? "bot-msg" : "user-msg")
    msgDiv.appendChild(msgBoxDiv)

    // Creates the message inside the container
    const messageP = document.createElement("p")
    messageP.classList.add("message-text")
    msgBoxDiv.appendChild(messageP)
    
    
    // Adds to the end of the message holder
    messageHolder.appendChild(msgDiv)
    let lastChar = 0
    const typewriter = () => {

        // If it's not the last message, then don't type out
        if (index < responseLength-1) {
            messageP.textContent = messageDetails.message
            return;
        }

        // Types out each character
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

    // Scrolls to the bottom
    messageHolder.scrollTo(0, messageHolder.scrollHeight)
}