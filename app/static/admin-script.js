
// A function to load the survey charts
async function loadSurveyCharts() {
    try {
        const response = await fetch('/survey-results');
        if (!response.ok) throw new Error('Failed to fetch survey data.');

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        const container = document.getElementById('charts-container');
        container.innerHTML = ''; // Clear existing charts

        // Questions for the charts and data variables
        const questions = [
            { label: 'How satisfied are you with your answers?', data: data.q1_counts, color: 'rgba(75, 192, 192, 0.6)' },
            { label: 'How helpful was the advice?', data: data.q2_counts, color: 'rgba(192, 75, 192, 0.6)' },
            { label: 'Would you recommend this chatbot to others?', data: data.q3_counts, color: 'rgba(192, 192, 75, 0.6)' },
        ];

        questions.forEach((question, index) => {
            // Create a canvas element for each chart
            const chartWrapper = document.createElement('div');
            chartWrapper.style.marginBottom = '20px';
            const canvas = document.createElement('canvas');
            canvas.id = `chart-${index + 1}`;
            chartWrapper.appendChild(canvas);
            container.appendChild(chartWrapper);

            // Get labels and data for the chart
            const labels = Object.keys(question.data);
            const chartData = Object.values(question.data);

            // Create the chart
            const ctx = canvas.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: question.label,
                            data: chartData,
                            backgroundColor: question.color,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                        },
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        });
    } catch (error) {
        console.error('Error loading survey charts:', error);
    }
}

// A function to load the response time chart
async function loadResponseTimeChart() {
    try {
        const response = await fetch('/response-times');
        if (!response.ok) throw new Error('Failed to fetch response times.');

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        const times = data.times;
        const avg = data.average_time;

        // Prepare data for a scatter plot. Each data point must have x and y values.
        const scatterData = times.map((time, index) => ({ x: index + 1, y: time }));

        const ctx = document.getElementById('response-time-chart').getContext('2d');
        new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Response Time',
                        data: scatterData,
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',

                    },
                ],
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: `Average Response Time: ${avg.toFixed(2)} seconds`
                    },
                    legend: {
                        display: true,
                        position: 'top',
                    },
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: {
                            display: true,
                            text: 'Response number'
                        },
                        beginAtZero: true,
                    },
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Time'
                        },
                    },
                },
            },
        });
    } catch (error) {
        console.error('Error loading response time chart:', error);
    }
}

// A function to load the word cloud
async function loadWordCloud() {
    try {
        const response = await fetch('/generate-wordcloud');
        if (!response.ok) throw new Error('Failed to fetch word cloud.');

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        const wordcloudImg = document.getElementById('wordcloud');
        wordcloudImg.src = data.wordcloud_url;
    } catch (error) {
        console.error('Error loading word cloud:', error);
    }
}

// Load all functions
loadSurveyCharts();
loadResponseTimeChart();
loadWordCloud();

