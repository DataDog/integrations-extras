<%page expression_filter="h"/>
<%inherit file="/desc_base.mako"/>
<%def name="title()">
  MongoDB Atlas Integration
</%def>

<div id="int-overview">
<h2>Overview</h2>
MongoDB Atlas can push calculated metrics into Datadog to:
<ul>
  <li>Visualize key MongoDB Atlas metrics.</li>
  <li>Correlate MongoDB Atlas performance with the rest of your applications.</li>
</ul>

</div>

<div id="int-configuration">
<h2>Configuration</h2>
  <p><em>You can install the MongoDB Atlas integration by logging into your Atlas portal.</em></p>

<ol>
    <li>Retrieve or create a Datadog <a href="/account/settings#api">API key</a>.
    <li>In the Atlas portal, enter a Datadog API key under <strong>Integrations</strong> -> <strong>Datadog Settings</strong>.
</ol>
</div>

<%include file="/metrics_list.mako"/>
