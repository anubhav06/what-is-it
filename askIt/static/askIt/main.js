document.addEventListener('DOMContentLoaded', function() {
    console.log('Loaded')

    document.addEventListener('click', event => {

        const element = event.target;
        console.log("clicked")
        // Get the clicked element id and check if it contains `answer-btn`
        if(element.id.indexOf('answer-btn') > -1){

            console.log('Clicked at edit btn')
            // Get the clicked element id and split the actuall id from `answer-btn`
            const id = element.id.split('answer-btn')[1]
            document.querySelector(`#question${id}`).style.display = `none`
            document.querySelector(`#answerQuestion${id}`).style.display = 'block'
        } 

    })

})