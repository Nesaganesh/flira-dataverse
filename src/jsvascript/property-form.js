function validateAskingPrice(executionContext) {

    // Get the current D365 form
    const formContext = executionContext.getFormContext();

    // Get Asking Price
    const askingPrice =
        formContext.getAttribute("flira_askingprice").getValue();

    // Remove previous notifications
    formContext.ui.clearFormNotification("LOW_PRICE");
    formContext.ui.clearFormNotification("HIGH_PRICE");

    // User hasn't entered a price yet
    if (askingPrice === null) {
        return;
    }

    // Low price
    if (askingPrice < 100000) {

        formContext.ui.setFormNotification(
            "Warning: Asking Price is below £100,000.",
            "WARNING",
            "LOW_PRICE"
        );

        return;
    }

    // High-value property
    if (askingPrice >= 1000000) {

        formContext.ui.setFormNotification(
            "High Value Property: Asking Price is £1,000,000 or above.",
            "INFO",
            "HIGH_PRICE"
        );
    }
}