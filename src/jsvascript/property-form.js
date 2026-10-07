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

// ======================================================
// UK Postcode Validation
// ======================================================

function validatePostcode(executionContext) {

    const formContext = executionContext.getFormContext();

    const postcodeAttribute =
        formContext.getAttribute("flira_postcode");

    const postcode = postcodeAttribute.getValue();

    // Remove old notification
    formContext.ui.clearFormNotification("INVALID_POSTCODE");

    // Nothing entered - don't validate
    if (!postcode) {
        return;
    }

    // Remove leading/trailing spaces and convert to uppercase
    const cleanedPostcode = postcode
        .trim()
        .toUpperCase();

    // UK postcode validation
    const postcodeRegex =
        /^[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}$/;

    if (!postcodeRegex.test(cleanedPostcode)) {

        formContext.ui.setFormNotification(
            "Invalid UK postcode. Example: IP1 2AB",
            "ERROR",
            "INVALID_POSTCODE"
        );

        return;
    }

    // Format postcode so there is one space before last 3 characters
    const formattedPostcode =
        cleanedPostcode.replace(/\s+/g, "");

    const finalPostcode =
        formattedPostcode.slice(0, -3) +
        " " +
        formattedPostcode.slice(-3);

    // Put formatted postcode back into the field
    postcodeAttribute.setValue(finalPostcode);
}


// ======================================================
// Retrieve Properties from Dataverse
// ======================================================

function retrieveProperties(executionContext) {

    const formContext = executionContext.getFormContext();

    Xrm.WebApi.retrieveMultipleRecords(
        "flira_property",
        "?$select=flira_name,flira_towncity,flira_postcode,flira_askingprice&$top=5"
    ).then(

        function success(result) {

            console.log(
                "Properties returned:",
                result.entities.length
            );

            result.entities.forEach(function (property) {

                console.log("--------------------");

                console.log(
                    "Name:",
                    property.flira_name
                );

                console.log(
                    "Town:",
                    property.flira_towncity
                );

                console.log(
                    "Postcode:",
                    property.flira_postcode
                );

                console.log(
                    "Asking Price:",
                    property.flira_askingprice
                );
            });

            formContext.ui.setFormNotification(
                result.entities.length +
                    " properties retrieved from Dataverse. Check browser console.",
                "INFO",
                "PROPERTY_RETRIEVE"
            );
        },

        function error(error) {

            console.error(
                "Dataverse error:",
                error.message
            );

            formContext.ui.setFormNotification(
                "Unable to retrieve Properties: " +
                    error.message,
                "ERROR",
                "PROPERTY_RETRIEVE_ERROR"
            );
        }
    );
}