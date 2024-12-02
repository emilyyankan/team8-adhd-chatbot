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
        container.innerHTML = ''; // Clear existing charts if any

        // Chart data for each question
        const questions = [
            { label: 'How satisfied are you with your answers?', data: data.q1_counts, color: 'rgba(75, 192, 192, 0.6)' },
            { label: 'How helpful was the advice?', data: data.q2_counts, color: 'rgba(192, 75, 192, 0.6)' },
            { label: 'Would you recommend this chatbot to others?', data: data.q3_counts, color: 'rgba(192, 192, 75, 0.6)' },
        ];

        questions.forEach((question, index) => {
            // Create a new canvas element for each chart
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

// Load charts
loadSurveyCharts();

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

// Load word cloud
loadWordCloud();

