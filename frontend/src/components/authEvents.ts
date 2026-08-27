export const OPEN_SIGNIN_EVENT = 'ff-signin-open'

export function openSignIn(): void {
  window.dispatchEvent(new Event(OPEN_SIGNIN_EVENT))
}
