import {
  AuthenticatedTemplate,
  UnauthenticatedTemplate,
  useMsal,
} from '@azure/msal-react';
import { loginRequest } from '../authConfig';
import { callMsGraph } from '../utils/MsGraphApi';

export const SignInSignOutButton = () => {
  const { instance } = useMsal();

  const handleLogin = (loginType: string) => {
    if (loginType === 'popup') {
      instance.loginPopup(loginRequest);
    } else if (loginType === 'redirect') {
      instance.loginRedirect(loginRequest);
    }
  };

  const handleCallMsGraph = () => {
    callMsGraph().then((response) => console.log(response));
  };

  return (
    <>
      <UnauthenticatedTemplate>
        Please sign-in to see your profile information.
        <div>
          <button
            type="button"
            className="hidden rounded bg-green-500 px-4 py-2 text-sm font-bold text-white hover:bg-green-400 md:block"
            onClick={() => handleLogin('popup')}
            key="loginPopup"
          >
            Sign in using Popup
          </button>
          <button
            type="button"
            className="hidden rounded bg-blue-500 px-4 py-2 text-sm font-bold text-white hover:bg-blue-400 md:block"
            onClick={() => handleLogin('redirect')}
            key="loginRedirect"
          >
            Sign in using Redirect
          </button>
        </div>
      </UnauthenticatedTemplate>
      <AuthenticatedTemplate>
        <div>
          <h1>Profile Information</h1>
          <p>Below is the information from your profile.</p>
          <div>
            <button
              type="button"
              className="rounded bg-blue-500 px-4 py-2 text-sm font-bold text-white hover:bg-blue-400"
              onClick={() => instance.logout()}
              key="logout"
            >
              Logout
            </button>
            <button
              type="button"
              className="rounded bg-blue-500 px-4 py-2 text-sm font-bold text-white hover:bg-blue-400"
              onClick={() => handleCallMsGraph()}
              key="logout"
            >
              Call MS Graph
            </button>
          </div>
        </div>
      </AuthenticatedTemplate>
    </>
  );
};
