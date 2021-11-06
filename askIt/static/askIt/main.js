document.addEventListener('DOMContentLoaded', function() {

    var spyImageOneCount = 0;

    document.addEventListener('click', event => {

        const element = event.target;
        // Get the clicked element id and check if it contains `answer-btn`
        if(element.id.indexOf('answer-btn') > -1){

            console.log('Clicked at edit btn')
            // Get the clicked element id and split the actuall id from `answer-btn`
            const id = element.id.split('answer-btn')[1]
            document.querySelector(`#answerQuestion${id}`).style.display = 'block'
        } 

        if(element.id == "spyImageOne"){
            spyImageOneCount += 1;
        }

        if(spyImageOneCount == 5){
            document.querySelector('#hintOne').style.backgroundColor = "white";
        }

    })

})