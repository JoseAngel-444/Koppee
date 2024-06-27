$(document).ready(function() {
    $('#opinion-form').submit(function(event) {
        event.preventDefault();
        var opinionText = $('#opinion-text').val();
        var newOpinionHTML = `
            <div class="testimonial-item">
                <div class="d-flex align-items-center mb-3">
                    <img class="img-fluid rounded-circle mb-3 mb-sm-0" src="{{url_for('static',filename='/img/default-avatar.jpg')}}" alt="">
                    <div class="ml-3">
                        <h4>Anonymous</h4>
                        <i>Cliente</i>
                    </div>
                </div>
                <p class="m-0">${opinionText}</p>
            </div>
        `;
        $('#new-opinion-container').append(newOpinionHTML);
        $('#opinion-text').val('');
    });
});
