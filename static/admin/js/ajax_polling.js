(function () {
    var status = $('.status'),
        poll = function () {
            $.ajax({
                url: 'status.json',
                dataType: 'json',
                type: 'get',
                success: function (data) { // check if available
                    if (data.number_of_emails_sent !== 0 && data.number_of_emails_sent <= data.number_of_total_emails) {
                        status.text('Sent ' + data.number_of_emails_sent + ' ' + 'of ' + data.number_of_total_emails + ' emails'
                                    + ' ' + data.number_of_not_sent_emails + ' emails have not been sent');
                        var elem = document.getElementById("myBar");
                        var width = 0;
                        var id = setInterval(frame, 1);

                        function frame() {
                            if (width >= data.number_of_total_emails) {
                                clearInterval(id);
                            } else {
                                clearInterval(id);
                                width = (data.number_of_emails_sent * 100) / data.number_of_total_emails;
                                elem.style.width = width + '%';
                                elem.innerHTML = '' + Math.trunc(width) + '%';
                            }
                        }
                    }
                },
            });
        },
        pollInterval = setInterval(function () { // run function every 2000 ms
            poll();
        }, 10000);
    poll(); // also run function on init
})();