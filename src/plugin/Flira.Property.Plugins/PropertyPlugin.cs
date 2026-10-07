using System;
using Microsoft.Xrm.Sdk;

namespace Flira.Property.Plugins;

public class PropertyPlugin : IPlugin
{
    public void Execute(IServiceProvider serviceProvider)
    {
        // -------------------------------------------------------
        // 1. Get Dataverse services
        // -------------------------------------------------------

        ITracingService tracingService =
            (ITracingService?)serviceProvider.GetService(typeof(ITracingService))
            ?? throw new InvalidPluginExecutionException(
                "Tracing service is unavailable."
            );

        IPluginExecutionContext context =
            (IPluginExecutionContext?)serviceProvider.GetService(
                typeof(IPluginExecutionContext)
            )
            ?? throw new InvalidPluginExecutionException(
                "Plugin execution context is unavailable."
            );

        tracingService.Trace(
            $"PropertyPlugin started. Message: {context.MessageName}, Stage: {context.Stage}"
        );


        // -------------------------------------------------------
        // 2. Get the Target record
        // -------------------------------------------------------

        if (!context.InputParameters.Contains("Target"))
        {
            tracingService.Trace(
                "PropertyPlugin: InputParameters does not contain Target."
            );

            return;
        }

        if (context.InputParameters["Target"] is not Entity property)
        {
            tracingService.Trace(
                "PropertyPlugin: Target is not an Entity."
            );

            return;
        }


        // -------------------------------------------------------
        // 3. Make sure this is the Property table
        // -------------------------------------------------------

        if (property.LogicalName != "flira_property")
        {
            tracingService.Trace(
                $"PropertyPlugin: Ignoring table {property.LogicalName}."
            );

            return;
        }


        // -------------------------------------------------------
        // 4. Logical column names
        // -------------------------------------------------------

        const string YearBuiltField = "flira_yearbuilt";
        const string PropertyAgeField = "flira_propertyage";


        // -------------------------------------------------------
        // 5. Check whether Year Built was supplied
        // -------------------------------------------------------

        if (!property.Attributes.Contains(YearBuiltField))
        {
            tracingService.Trace(
                "PropertyPlugin: Year Built was not supplied."
            );

            return;
        }

        int? yearBuilt =
            property.GetAttributeValue<int?>(YearBuiltField);

        if (!yearBuilt.HasValue)
        {
            tracingService.Trace(
                "PropertyPlugin: Year Built is empty."
            );

            return;
        }


        // -------------------------------------------------------
        // 6. Validate Year Built
        // -------------------------------------------------------

        int currentYear = DateTime.UtcNow.Year;

        if (yearBuilt.Value < 1800)
        {
            throw new InvalidPluginExecutionException(
                "Year Built cannot be earlier than 1800."
            );
        }

        if (yearBuilt.Value > currentYear)
        {
            throw new InvalidPluginExecutionException(
                $"Year Built cannot be greater than {currentYear}."
            );
        }


        // -------------------------------------------------------
        // 7. Calculate Property Age
        // -------------------------------------------------------

        int propertyAge =
            currentYear - yearBuilt.Value;


        // -------------------------------------------------------
        // 8. Put calculated value onto the Target
        // -------------------------------------------------------

        property[PropertyAgeField] = propertyAge;

        tracingService.Trace(
            $"PropertyPlugin: Year Built = {yearBuilt.Value}, " +
            $"Property Age = {propertyAge}."
        );
    }
}