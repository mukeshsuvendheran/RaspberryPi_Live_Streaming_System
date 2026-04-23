// d = new Dialog("Hello World", "Quote not loaded, click Show Quote button to motivate you.", {
//     "backdrop": "static"
// });

// d.setButtons([
//     {
//         name: "Show Quote",
//         class: "btn-primary",
//         onClick: function(event){
//             console.log(event);
//             var settings = {
//                 "url": "https://type.fit/api/quotes",
//                 "method": "GET",
//                 "timeout": 0,
//               };
              
//             $.ajax(settings).done(function (response) {
//                 console.log(response);
//                 var items = JSON.parse(response);
//                 var quote = items[Math.floor(Math.random()*items.length)];
//                 var template = `<figure>
//                     <blockquote class="blockquote text-center">
//                     <p class="ps-2">${quote.text}</p>
//                     </blockquote>
//                     <figcaption class="blockquote-footer text-center">
//                     <cite title="Source Title">${quote.author}</cite>
//                     </figcaption>
//                 </figure>`;
//                 $(event.data.modal).find(".modal-body").html(template);
//             });
//         }
//     },
//     {
//         name: "Close",
//         class: "btn-warning",
//         // dismiss: true,
//         onClick: function(event){
//             $(event.data.modal).modal('hide');
//         }
//     }
// ]);

// d.show();

const animateCSS = (element, animation, prefix = 'animate__') =>
  // We create a Promise and return it
  new Promise((resolve, reject) => {
    const animationName = `${prefix}${animation}`;
    const node = document.querySelector(element);

    node.classList.add(`${prefix}animated`, animationName);

    // When the animation ends, we clean the classes and resolve the Promise
    function handleAnimationEnd(event) {
      event.stopPropagation();
      node.classList.remove(`${prefix}animated`, animationName);
      resolve('Animation ended');
    }

    node.addEventListener('animationend', handleAnimationEnd, {once: true});
  });

$('.btn-add-device').on('click', function(){
    $.get("/devices/add", function(data, status, xhr){
        if(status == "success"){
            d = new Dialog("Add Device", data);
            d.setButtons([
                {
                    "name": "Register",
                    "class": "btn-success btn-register-device",
                    "onClick": function(event){
                        modal = $(event.data.modal);
                        $.post('/api/devices/register', {
                            name: modal.find('#device-name').val(),
                            type: modal.find('#device-type').val(),
                            api: modal.find('#device-api').val(),
                            remarks: modal.find('#device-remarks').val()
                        }, function(data, status, xhr){
                            if(status == "success"){
                                t = new Toast("Device Registered", "now", "Device has been registered successfully.");
                                t.show();
                                $('#devices_index row').append(data);
                            }
                            $(event.data.modal).modal('hide');
                        }).fail(function(xhr, status, error){
                            console.log(xhr);
                            t = new Toast("Error", "now", xhr.responseJSON.error);
                            t.show();
                        });
                    }
                },
                {
                    "name": "Cancel",
                    "class": "btn-secondary",
                    "dismiss": true
                }
            ]);
            d.show();
        }
    });
});

$('.btn-add-api-key').on('click', function(){
    $.get('/api/dialogs/api_keys', function(data, status, xhr){
        d = new Dialog("Add API Key", data);
        d.setButtons([
            {
                "name": "Generate Key",
                "class": "btn-success btn-generate-key",
                "onClick": function(event){
                    var modal = $(event.data.modal);
                    var name = modal.find('#api-name').val();
                    var group = modal.find('#api-group').val();
                    var remarks = modal.find('#api-remarks').val();

                    if(name.length <=3 || group.length <= 3){
                        // alert("API name and group cannot be empty");
                        animateCSS('.btn-generate-key', 'headShake')
                        return;
                    } else {
                        $.post('/api/v1/create/key', {
                            'name': name,
                            'group': group,
                            'remarks': remarks
                        }, function(data, status, xhr){
                            if(status == 'success'){
                                var modal = $(event.data.modal);
                                $(modal).modal('hide');
                                key = new Dialog("API Key", data.key);
                                key.show();
                                $.get('/api_keys/row?hash='+data.hash, function(data, status, xhr){
                                    if(status=="success"){
                                        $("#api_key_table").append(data);
                                        addApiKeyRowListeners();
                                        //TODO: Check if we need to reinitialize click event for delete button, since its dynamically added to DOM.
                                    }
                                });
                            } else {
                                alert(data.message);
                            }
                        });
                    }
                }
            },
            {
                "name": "Dismiss",
                "class": "btn-secondary",
                "dismiss": true
            }
        ])
        d.show();
    });
});

function addApiKeyRowListeners(){
    $('.btn-api-enable').off('click');
    $('.btn-api-enable').on('click', function(){
        var id = $(this).attr('id');
        var status = $(this).is(':checked');
        var row = $(this).parent().parent().parent();
        console.log(row);
        $.post('/api_keys/enable', {
            'id': id,
            'status': status
        }, function(data, status, xhr){
            if(data.status){
                $(row).find('.api-status-badge').removeClass('bg-gradient-secondary').addClass('bg-gradient-success').html('ACTIVE');
            } else {
                $(row).find('.api-status-badge').removeClass('bg-gradient-success').addClass('bg-gradient-secondary').html('INACTIVE');
            }
        });
    });
    
    $('.btn-delete-api-key').off('click');
    $('.btn-delete-api-key').on('click', function(){
        var rowid = $(this).attr('data-rowid');
        $.get('/api_keys/row/delete_dialog?hash='+rowid, function(data, status, xhr){
            d = new Dialog("Delete API Key", data);
            d.setButtons([
                {
                    "name": "Delete",
                    "class": "btn-danger btn-delete-key",
                    "onClick": function(event){
                        $.get('/api_keys/row/delete?hash='+rowid, function(data, status, xhr){
                            if(status == 'success'){
                                var modal = $(event.data.modal);
                                $(modal).modal('hide');
                                $('#row-'+rowid).remove();
                            }
                        })
                    }
                },
                {
                    "name": "Cancel",
                    "class": "btn-secondary",
                    "dismiss": true
                }
            ])
            d.show();
        })
    });
}

addApiKeyRowListeners();

$('.btn-add-api-group').on('click', function(){
    d = new Dialog("Add Group", `
    <form>
        <div class="form-group">
            <label for="group-name">Group Name</label>
            <input type="text" class="form-control" id="group-name" placeholder="Cameras">
        </div>
        <div class="form-group">
            <label for="group-desc">Description</label>
            <textarea class="form-control" id="group-desc" rows="2"></textarea>
        </div>
    </form>
    `);
    d.setButtons([
        {
            "name": "Add Group",
            "class": "btn-success btn-add-group",
            "onClick": function(event){
                var modal = $(event.data.modal);
                console.log(modal);
                var groupName = modal.find('#group-name').val();
                var groupDesc = modal.find('#group-desc').val();
                if(groupName.length <=3 || groupDesc.length <= 5){
                    // alert("Group name cannot be empty");
                    animateCSS('.btn-add-group', 'headShake')
                    return;
                } else {
                    $.post('/api/v1/create/group', {
                        'name': groupName,
                        'description': groupDesc
                    }, function(data, status, xhr){
                        if(data.status == 'success'){
                            var modal = $(event.data.modal);
                            $(modal).modal('hide');
                        } else {
                            // alert(data.message);
                        }
                    });
                }
            }
        },
        {
            "name": "Cancel",
            "class": "btn-secondary",
            "onClick": function(event){
                var modal = $(event.data.modal);
                $(modal).modal('hide');
            }
        }
    ]);
    d.show();

});

function apiCall(){
    //do network calls and fetch more images
    return `
    <li><img src="https://picsum.photos/id/1/5000/3333" alt="Picture 1"></li>
    <li><img src="https://picsum.photos/id/4/5000/3333" alt="Picture 2"></li>
    <li><img src="https://picsum.photos/id/7/4728/3168" alt="Picture 3"></li>
    <li><img src="https://picsum.photos/id/1/5000/3333" alt="Picture 1"></li>
    <li><img src="https://picsum.photos/id/4/5000/3333" alt="Picture 2"></li>
    <li><img src="https://picsum.photos/id/7/4728/3168" alt="Picture 3"></li>
    `
}

const images = document.getElementById('images');
const viewer = new Viewer(images, {
    loop: true,
    interval: 500,
    view: function(event){
        console.log((event.detail.index + 1) + " / " +viewer.length);
        var cur_image = event.detail.index + 1;
        var length = viewer.length;
        var leftover = 1;
        
        if(length - cur_image <= leftover){
            console.log("now we can add more images");
            $(images).append(apiCall());
            viewer.update();
        }
    }
});

$('#raspi-cam-1').on('click', function(e){
    viewer.show();
});

$(".mousetest").on('mouseenter', function(e){
    console.log("mouse entered");
});

$(".mousetest").on('mouseleave', function(e){
    console.log("mouse exited");
});

if (window.location.pathname.startsWith('/devices/mcamera')) {
    var device_id = window.location.pathname.split('/').reverse()[0];
    console.log("Acquiring about "+ device_id);
    setInterval(function(){
        $.get('/api/motion/latest/'+device_id, function(data){
            $('#latest-image').attr('src', data.uri)
        })
    }, 1000);
}



