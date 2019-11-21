window.addEventListener("load", (e) => {

     $('#schema_distribution_select').on("change", function () {
         var value = $(this).find("option:selected").val();
         $.getJSON(`/schema_distribution/${value}`, data => {
            Plotly.newPlot('schemas_distribution_data', data, {});
        })
     });

     $('#entity_attributes_population_select').on("change", function () {
         var value = $(this).find("option:selected").val();
         $.getJSON(`/entity_attributes_population/${value}`, data => {
            Plotly.newPlot('entity_attributes_population_graph', data, {});
        })
     });
});