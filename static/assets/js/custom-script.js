$(document).on("click", ".add-form-row", function (e) {
    e.preventDefault();
    cloneMore("table tr:last", "form");
    return false;
});

$(document).on("click", ".remove-form-row", function (e) {
    e.preventDefault();
    deleteForm("form", $(this));
    return false;
});

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp("(" + prefix + "-\\d+)");
    var replacement = prefix + "-" + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function cloneMore(selector, prefix) {
    var newElement = $(selector).clone(true);
    console.log(newElement);
    var total = $("#id_" + prefix + "-TOTAL_FORMS").val();
    newElement.find(":input:not([type=button]):not([type=submit]):not([type=reset])").each(function () {
        var name = $(this).attr("name");
        if (name) {
            name = name.replace("-" + (total - 1) + "-", "-" + total + "-");
            var id = "id_" + name;
            $(this).attr({ name: name, id: id }).val("").removeAttr("checked");
        }
    });
    newElement.find("label").each(function () {
        var forValue = $(this).attr("for");
        if (forValue) {
            forValue = forValue.replace("-" + (total - 1) + "-", "-" + total + "-");
            $(this).attr({ for: forValue });
        }
    });
    total++;
    $("#id_" + prefix + "-TOTAL_FORMS").val(total);
    $(selector).after(newElement);
    $("div.form-row.button.is-primary").not(":last").hide();
    //var conditionRow = $('.form-row:not(:last)');
    //  conditionRow.find('.button.is-primary')
    // conditionRow.hide();
    // conditionRow.removeClass('btn-success').addClass('btn-danger')
    // conditionRow.removeClass('add-form-row').addClass('remove-form-row')
    // conditionRow.html('-');
    // return false;
}
function deleteForm(prefix, btn) {
    var total = parseInt($("#id_" + prefix + "-TOTAL_FORMS").val());
    if (total > 1) {
        btn.closest(".form-row").remove();
        var forms = $(".form-row");
        $("#id_" + prefix + "-TOTAL_FORMS").val(forms.length);
        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i))
                .find(":input")
                .each(function () {
                    updateElementIndex(this, prefix, i);
                });
        }
    }
    return false;
}


$("table input").on("input", function () {
    var total = [];
    var $tr = $(this).closest("tr");
    var textValue1 = $("input.rate", $tr).val();
    var textValue2 = $("input.quantity", $tr).val();
    amt = textValue1 * textValue2;
    //console.log(amt);
    $(".amount", $tr).html(amt);
    calc_total();
    calc_tax();
});
//total
function calc_total() {
    var sum = 0;
    $(".amount").each(function () {
        sum += parseFloat($(this).text());
    });
    $("#total").text(sum);
    console.log(sum);
}
//tax
function calc_tax() {
    $("#gst").on("change", function () {
        //Getting Value
        var selValue = $("#gst").val();
        //Setting Value
        if (this.selValue == "0") {
            $("#total1").hide();
        } else {
            $("#total1").show();
        }
        var taxa = selValue;
        $(".amount").each(function () {
            taxa *= parseFloat($(this).text());
        });
        calc_total();
        $("#total1").text(taxa.toFixed(2));
        //var bbb = taxa.toFixed(2);
    });
}


function bodyloadfirst() {
    document.getElementById("div1a").style.display = "block";
    document.getElementById("div1b").style.display = "none";
    document.getElementById("div1c").style.display = "none";
    document.getElementById("div1d").style.display = "none";
    document.getElementById("aprorigsimage").style.display = "block";
    document.getElementById("aproitimage").style.display = "none";
    document.getElementById("aprocmsimage").style.display = "none";
    document.getElementById("aprohostingimage").style.display = "none";
    document.getElementById("div2A").style.display = "block";
    document.getElementById("div2B").style.display = "none";
    document.getElementById("div2C").style.display = "none";
    document.getElementById("div2D").style.display = "none";
}
function show1() {
    document.getElementById("div1a").style.display = "block";
    document.getElementById("div1b").style.display = "none";
    document.getElementById("div1c").style.display = "none";
    document.getElementById("div1d").style.display = "none";
    document.getElementById("aprorigsimage").style.display = "block";
    document.getElementById("aproitimage").style.display = "none";
    document.getElementById("aprocmsimage").style.display = "none";
    document.getElementById("aprohostingimage").style.display = "none";
    document.getElementById("div2A").style.display = "block";
    document.getElementById("div2B").style.display = "none";
    document.getElementById("div2C").style.display = "none";
    document.getElementById("div2D").style.display = "none";
}
function show2() {
    document.getElementById("div1a").style.display = "none";
    document.getElementById("div1b").style.display = "block";
    document.getElementById("div1c").style.display = "none";
    document.getElementById("div1d").style.display = "none";
    document.getElementById("aprorigsimage").style.display = "none";
    document.getElementById("aproitimage").style.display = "block";
    document.getElementById("aprocmsimage").style.display = "none";
    document.getElementById("aprohostingimage").style.display = "none";
    document.getElementById("div2A").style.display = "none";
    document.getElementById("div2B").style.display = "block";
    document.getElementById("div2C").style.display = "none";
    document.getElementById("div2D").style.display = "none";
}
function show3() {
    document.getElementById("div1a").style.display = "none";
    document.getElementById("div1b").style.display = "none";
    document.getElementById("div1c").style.display = "block";
    document.getElementById("div1d").style.display = "none";
    document.getElementById("aprorigsimage").style.display = "none";
    document.getElementById("aproitimage").style.display = "none";
    document.getElementById("aprocmsimage").style.display = "block";
    document.getElementById("aprohostingimage").style.display = "none";
    document.getElementById("div2A").style.display = "none";
    document.getElementById("div2B").style.display = "none";
    document.getElementById("div2C").style.display = "block";
    document.getElementById("div2D").style.display = "none";
}
function show4() {
    document.getElementById("div1a").style.display = "none";
    document.getElementById("div1b").style.display = "none";
    document.getElementById("div1c").style.display = "none";
    document.getElementById("div1d").style.display = "block";
    document.getElementById("aprorigsimage").style.display = "none";
    document.getElementById("aproitimage").style.display = "none";
    document.getElementById("aprocmsimage").style.display = "none";
    document.getElementById("aprohostingimage").style.display = "block";
    document.getElementById("div2A").style.display = "none";
    document.getElementById("div2B").style.display = "none";
    document.getElementById("div2C").style.display = "none";
    document.getElementById("div2D").style.display = "block";
}