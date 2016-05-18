$(document).ready(function () {
// passing a fixedOffset param will cause the table header to stick to the bottom of this element
$("table").stickyTableHeaders({ scrollableArea: $(".scrollable-area")[0]});
});
