var chart = document.getElementById("covid-graph").getContext("2d");
var line_graph = new Chart(chart, {
    type: "line",
    data: {
        labels: [
            {% for i in dict_list %}
                "{{ i['time'] }}"
            {% endfor %}
        ],
        datasets: [{
          label: "Number of Cases",
          backgroundColor: "rgba(0,0,0,1.0)",
          borderColor: "rgba(0,0,0,0.1)",
          data: [
            {% for i in dict_list %}
               "{{ i['total'] }}",
              {% endfor %}
	         ]
          }]
    },
    options: {
        responsive: false
    }

});