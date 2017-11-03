$(function() {
    function successResponse(response)
    {
        console.log(response);
        $('#btnLoadMore').removeClass('loading');
        $('#btnLoadMore').html("Load more");
        if (response.has_more)
            $('#btnLoadMore').addClass('has_more');
        else
            $('#btnLoadMore').removeClass('has_more');

        $('#btnLoadMore').attr("disabled", false);

        if (response.items) {
            for (var i = 0; i < response.items.length; i++) {
                $('#post_template .profile_image img').attr("src", response.items[i].owner.profile_image);
                $('#post_template .display_name').html(response.items[i].owner.display_name);
                $('#post_template .owner').attr("title", "Visit " + response.items[i].owner.display_name);
                $('#post_template .owner').attr("onclick", "window.open('" + response.items[i].owner.link + "')");

                $('#post_template .post_type').html(response.items[i].post_type);
                $('#post_template .title').html(response.items[i].title);
                $('#post_template .body').html(response.items[i].body);
                $('#post_template .post').attr("title", "View post");
                $('#post_template .post').attr("onclick", "window.open('" + response.items[i].link + "')");

                var post = $('#post_template').html();
                $('#posts').append(post);
            }

            $('#querypos').val(response.query_pos + response.items.length);
        }
        else
        {
            $.simplyToast("No posts!", 'warning');
        }
    }

    function errorResponse(error)
    {
        $('#btnLoadMore').removeClass('loading');
        $('#btnLoadMore').html("Load more");
        $('#btnLoadMore').removeClass('has_more');
        $('#btnLoadMore').attr("disabled", false);
        if (error.responseJSON) {
            console.log(error.responseJSON);
            $.simplyToast("error_id: " + error.responseJSON.error_id + "<br>error_name: " + error.responseJSON.error_name + "<br>error_message: " + error.responseJSON.error_message, 'danger');
        }
        else {
            console.log(error);
            $.simplyToast("Seems connection error(" + error.statusText + ")", 'danger');
        }
    }

    $('#btnGetPosts').click(function() {
        $('#posts').html("");
        $('#btnLoadMore').addClass('loading');
        $('#btnLoadMore').html("Loading...");
        $('#btnLoadMore').attr("disabled", true);
        $.ajax({
            url: 'getposts',
            data: {uid:$('#uid').val(),querypos:1,pagesize:10},
            type: 'POST',
            dataType: 'JSON',
            success: function(response) {
                successResponse(response);
            },
            error: function(error) {
                errorResponse(error);
            }
        });
    });

    $('#btnLoadMore').click(function() {
        $('#btnLoadMore').addClass('loading');
        $('#btnLoadMore').html("Loading...");
        $('#btnLoadMore').attr("disabled", true);
        $.ajax({
            url: 'getposts',
            data: {uid:$('#uid').val(),querypos:$('#querypos').val(),pagesize:5},
            type: 'POST',
            dataType: 'JSON',
            success: function(response) {
                successResponse(response);
            },
            error: function(error) {
                errorResponse(error);
            }
        });
    });

    // Attach click handler to login button
    $('#btnLogin').click(function() {

        // Make the authentication call, note that being in an onclick handler
        //   is important; most browsers will hide windows opened without a
        //   'click blessing'
        SE.authenticate({
            success: function(data) {
                alert(
                    'User Authorized with account id = ' +
                    data.networkUsers[0].account_id + ', got access token = ' +
                    data.accessToken
                );
            },
            error: function(data) {
                alert('An error occurred:\n' + data.errorName + '\n' + data.errorMessage);
            },
            networkUsers: true
        });
    });
});