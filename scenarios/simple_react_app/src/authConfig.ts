import { Configuration, PopupRequest } from '@azure/msal-browser';

// Config object to be passed to Msal on creation
export const msalConfig: Configuration = {
  auth: {
    clientId: 'a2b8efbc-4dd2-4261-b628-4e23f835b689',
    authority:
      'https://login.microsoftonline.com/10e23afc-5838-4670-aa68-e1337024b543',
    redirectUri: '/',
    postLogoutRedirectUri: '/',
  },
  system: {
    allowNativeBroker: false, // Disables WAM Broker
  },
};

// Add here scopes for id token to be used at MS Identity Platform endpoints.
export const loginRequest: PopupRequest = {
  scopes: ['User.Read'],
};

// Add here the endpoints for MS Graph API services you would like to use.
export const graphConfig = {
  graphMeEndpoint: 'https://graph.microsoft.com/v1.0/me',
};
