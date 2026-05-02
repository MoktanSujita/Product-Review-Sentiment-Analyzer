document.addEventListener("DOMContentLoaded", function(){

    new Chart(document.getElementById('sentimentChart'),{
        type : 'pie',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [
                    sentimentData.positive,
                    sentimentData.negative,
                    sentimentData.neutral
                ],
                backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
            }]
        }
    });
});