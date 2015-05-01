// Handy functions
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, nbr) {
            return typeof args[nbr] != 'undefined' ? args[nbr] : match;
        });
    };
}
function log(o) { console.log(JSON.stringify(o)) }

function loadJSON(path, data_processing_fct) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            data_processing_fct(JSON.parse(xhr.responseText));
        }
    };
    xhr.overrideMimeType("application/json");
    xhr.open("GET", path, true);
    xhr.send();
}
// NOTE: Instead of AJAX HTTP request, HTML5 provides a FileReader interface:
if (!(window.File && window.FileReader && window.FileList && window.Blob)) {
    alert('The File APIs are not fully supported in this browser.');
}

function get_all_input_values () {
    var inputs = document.getElementsByTagName('input');
    var input_dict = {}, index;
    for (index = 0; index < inputs.length; ++index) {
        var node = inputs[index];
        if (node.type && node.type == 'checkbox') {
            value = node.checked;
        } else {
            value = node.value;
        }
        input_dict[node.name] = value;
    }
    return input_dict;
}

function save_inputs_to_file() {
    var answers_list = get_all_input_values();
    var date_str = (new Date()).toString()
    var answers = {answers:answers_list, date:date_str}

    // Prompt user to save the file
    location.href = "data:application/octet-stream," + encodeURIComponent(JSON.stringify(answers));
    // The .bin file can then be pretty-printed with 'python -mjson.tool'
}
