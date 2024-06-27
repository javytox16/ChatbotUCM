class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatbox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),

        }

        this.state= false;
        this.message = [{ name: "Bot", message: "¡Hola! ¿En qué puedo ayudarte hoy?" }];
    }

    display(){
        const {openButton, chatbox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatbox))

        sendButton.addEventListener('click', () => this.onSendButton(chatbox))

        const node = chatbox.querySelector('input');
        node.addEventListener('keyup', ({key}) => {
            if(key === "Enter"){
                this.onSendButton(chatbox);
            }
        })
    }

    toggleState(chatbox){
        this.state = !this.state;

        if (this.state){
            chatbox.classList.add('chatbox--active');
        } else{
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox){
        var textfield = chatbox.querySelector('input');
        let text1 = textfield.value;
        if (text1 === ""){
            return;
        }

        let msg1 = { name: "User", message: text1};
        this.message.push(msg1);

        fetch ($SCRIPT_ROOT + '/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(response => {
            let msg2 = {name: "Bot", message: response.response};
            this.message.push(msg2);
            this.updateChatText(chatbox)
            textfield.value = "";

            }).catch(error => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textfield.value = "";
            });

    }

    updateChatText(chatbox){
        var html = "";
        this.message.slice().reverse().forEach(function(item) {
            if (item.name === "Bot"){
                html += '<div class="messages__item messages__item--visitor">'+ item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">'+ item.message + '</div>';
            }
        });
    
        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
    
}
const chatbox = new Chatbox();
chatbox.display();