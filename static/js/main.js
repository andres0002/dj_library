var $ = jQuery.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);

	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});

	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		}
	}); 

	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});

	// Load Resize 
	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
		
	});
});
//My code.
function open_modal_creation(url){
	$('#creation').load(url, function(){
		$(this).modal('show');
	});
}

function open_modal_edition(url){
	$('#edition').load(url, function(){
		$(this).modal('show');
	});
}

function open_modal_elimination(url){
	$('#elimination').load(url, function(){
		$(this).modal('show');
	});
}

function close_modal_creation(){
	$('#creation').modal('hide');
}

function close_modal_edition(){
	$('#edition').modal('hide');
}

function close_modal_elimination(){
	$('#elimination').modal('hide');
}

function activeButtonCreation(){
	if ($('#button_creation').prop('disabled')){
		$('#button_creation').prop('disabled', false);
	}
	else{
		$('#button_creation').prop('disabled', true);
	}
}

function activeButtonEdition(){
	if ($('#button_edition').prop('disabled')){
		$('#button_edition').prop('disabled', false);
	}
	else{
		$('#button_edition').prop('disabled', true);
	}
}

function showCreationErrors(errors){
	$('#errors').html("");
	let error = '';
	for (let item in errors.responseJSON.error){
		error += '<div class="alert alert-danger">';
		error += '<strong>' + (
			item.toUpperCase() == "PASSWORD1"
				? 'PASSWORD' :
				item.toUpperCase() == "PASSWORD2"
					? 'CONFIRM PASSWORD'
					: item.toUpperCase() == "AUTHOR_ID"
						? "AUTHORS"
						: item.toUpperCase()
		) + ' (' + errors.responseJSON.error[item] + ')</strong>';
		error += '</div>';
	}
	$('#errors').append(error);
}

function showEditionErrors(errors){
	$('#errors_edition').html("");
	let error = '';
	for (let item in errors.responseJSON.error){
		error += '<div class="alert alert-danger">';
		error += '<strong>' + (
			item.toUpperCase() == "PASSWORD1"
				? 'PASSWORD' :
				item.toUpperCase() == "PASSWORD2"
					? 'CONFIRM PASSWORD'
					: item.toUpperCase() == "AUTHOR_ID"
						? "AUTHORS"
						: item.toUpperCase()
		) + ' (' + errors.responseJSON.error[item] + ')</strong>';
		error += '</div>';
	}
	$('#errors_edition').append(error);
}

function errorNotification(message){
	Swal.fire({
		title: '¡Error!',
		text: message,
		icon: 'error'
	})
}

function successNotification(message){
	Swal.fire({
		title: '¡Success!',
		text: message,
		icon: 'success'
	})
}

function infoNotification(message) {
	Swal.fire({
		title: '¡Information!',
		text: message,
		icon: 'info'
	});
}

function warningNotification(message) {
	Swal.fire({
		title: '¡Warning!',
		text: message,
		icon: 'warning'
	});
}

function debugNotification(message){
	Swal.fire({
		title: '¡Debug!',
		text: message,
		icon: 'error'
	})
}