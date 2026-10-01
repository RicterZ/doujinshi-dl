    //------------------------------------navbar script------------------------------------
var menu = document.getElementsByClassName("accordion");
for (var i = 0; i < menu.length; i++) {
  menu[i].addEventListener("click", function() {
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
	  this.classList.toggle("active");
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
	  this.classList.toggle("active");
    }
  });
}
var language = document.getElementById("language").children;
for (var i = 0; i < language.length; i++){
	language[i].addEventListener("click", function() {
		toggler = document.getElementById("language")
		toggler.style.maxHeight = null;
		document.getElementsByClassName("accordion")[0].classList.toggle("active");
		filter_maker(this.innerText, "language");
});
}
var category = document.getElementById("category").children;
for (var i = 0; i < category.length; i++){
	category[i].addEventListener("click", function() {
		document.getElementById("category").style.maxHeight = null;
		document.getElementsByClassName("accordion")[1].classList.toggle("active");
		filter_maker(this.innerText, "category");
});
}
//-----------------------------------------------------------------------------------
//----------------------------------Tags Script--------------------------------------
tag_maker(typeof tags === "undefined" ? {} : tags);

var tag = document.getElementsByClassName("btn-2");
for (var i = 0; i < tag.length; i++){
	tag[i].addEventListener("click", function() {
	filter_maker(this.innerText, this.id);
});
}

var input = document.getElementById("tagfilter");
input.addEventListener("input", function() {
	var tags = document.querySelectorAll(".btn-2");
	if (this.value.length > 0) {
        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
            var nome = tag.innerText;
            if (nome.toLowerCase().includes(this.value.trim().toLowerCase())) {
                tag.classList.remove("hidden");
		    }
			else {
				tag.classList.add("hidden");
            }
        }
    } else {
        for (var i = 0; i < tags.length; i++) {
            var tag = tags[i];
				tag.classList.add('hidden');
        }
    }
	filter_searcher();
});
input.addEventListener('keypress', function (e) {
	enter_search(e, this.value);
});
//-----------------------------------------------------------------------------------
//------------------------------------Functions--------------------------------------
function enter_search(e, input){
	var count = 0;
	var key = e.which || e.keyCode;
	if (key === 13 && input.length > 0) {
	  var all_tags = document.getElementById("tags").children;
	  for(i = 0; i < all_tags.length; i++){
		if (!all_tags[i].classList.contains("hidden")){
			count++;
			var tag_name = all_tags[i].innerText;
			var tag_id   = all_tags[i].id;
			if (count>1){break}
		}
	  }
	  if (count == 1){
		filter_maker(tag_name, tag_id);
	  }
	}
}
function filter_maker(text, class_value){
    var check = filter_checker(text);
	var nav_btn = document.getElementsByClassName("nav-btn")[0];
	if (nav_btn.classList.contains("hidden")){
	  nav_btn.classList.toggle("hidden");
	}
	if (check == true){
		var node = document.createElement("a");
		var textnode = document.createTextNode(text);
		node.appendChild(textnode);
		node.classList.add(class_value);
		nav_btn.appendChild(node);
		node.addEventListener("click", function() {
			this.remove();
			filter_searcher();
		});
		input.value = "";
		input.dispatchEvent(new Event("input"));
	}
}

function filter_searcher(){
	var query = input.value.trim().toLowerCase();
	var filters = document.getElementsByClassName("nav-btn")[0];
	var selected = Array.from(filters.children);
	filters.classList.toggle("hidden", selected.length === 0);
	var records = typeof data === "undefined" ? [] : data;
	var byFolder = new Map(records.map(function(record) {
		return [record.Folder, record];
	}));
	var galleries = document.getElementsByClassName("gallery-favorite");
	for (var i = 0; i < galleries.length; i++) {
		var gallery = galleries[i];
		var link = gallery.querySelector("a.cover");
		var folder = decodeURIComponent(link.getAttribute("href").slice(2, -11));
		var record = byFolder.get(folder) || {};
		var caption = gallery.querySelector(".caption").innerText;
		var title = record.title || caption;
		var matchesQuery = !query || title.toLowerCase().includes(query) ||
			caption.toLowerCase().includes(query) ||
			["artist", "tag", "parody", "character", "group"].some(function(field) {
				return (record[field] || []).some(function(value) {
					return value.toLowerCase().includes(query);
				});
			});
		var matchesFilters = selected.every(function(filter) {
			return (record[filter.className] || []).some(function(value) {
				return value.toLowerCase() === filter.innerText.toLowerCase();
			});
		});
		gallery.classList.toggle("hidden", !(matchesQuery && matchesFilters));
	}
}

function filter_checker(text){
    var filter_tags = document.getElementsByClassName("nav-btn")[0].children;
	if (filter_tags == null){return true;}
	for (var i=0; i < filter_tags.length; i++){
		if (filter_tags[i].innerText == text){return false;}
	}
	return true;
}

function tag_maker(data){
	for (i in data){
		for (j in data[i]){
			var node = document.createElement("button");
			var textnode = document.createTextNode(data[i][j]);
			node.appendChild(textnode);
			node.classList.add("btn-2");
			node.setAttribute('id', i);
			node.classList.add("hidden");
			document.getElementById("tags").appendChild(node);
		}
	}
}
