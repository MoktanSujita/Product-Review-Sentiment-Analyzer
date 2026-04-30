console.log("chart.js is running");
console.log("sentimentData:", sentimentData);

document.addEventListener("DOMContentLoaded", function(){

    const data = {
        labels: ['Positive', 'Negative', 'Neutral'],

        datasets: [{
            label: 'Reviews',
            data: [
                sentimentData.positive,
                sentimentData.negative,
                sentimentData.neutral
            ],
            backgroundColor: ['#4CAF50', '#F44336', '#FFC107']
        }]
    };
    new Chart(document.getElementById('sentimentChart'),{
        type : 'pie',
        data: data
    });
});