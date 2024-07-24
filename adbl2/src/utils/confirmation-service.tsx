// import * as React from "react";
// import { ConfirmationDialog, ConfirmationOptions } from "./ConfirmationDialog";

// const ConfirmationServiceContext = React.createContext<
//   (options: ConfirmationOptions) => Promise<void>
// >(Promise.reject);

// export const useConfirmation = () =>
//   React.useContext(ConfirmationServiceContext);

// export const ConfirmationServiceProvider = ({ children }) => {
//   const [
//     confirmationState,
//     setConfirmationState
//   ] = React.useState<ConfirmationOptions | null>(null);

//   const awaitingPromiseRef = React.useRef<{
//     resolve: () => void;
//     reject: () => void;
//   }>();

//   const openConfirmation = (options: ConfirmationOptions) => {
//     setConfirmationState(options);
//     return new Promise<void>((resolve, reject) => {
//       awaitingPromiseRef.current = { resolve, reject };
//     });
//   };

//   const handleClose = () => {
//     if (confirmationState.catchOnCancel && awaitingPromiseRef.current) {
//       awaitingPromiseRef.current.reject();
//     }

//     setConfirmationState(null);
//   };

//   const handleSubmit = () => {
//     if (awaitingPromiseRef.current) {
//       awaitingPromiseRef.current.resolve();
//     }

//     setConfirmationState(null);
//   };

//   return (
//     <>
//       <ConfirmationServiceContext.Provider
//         value={openConfirmation}
//         children={children}
//       />

//       <ConfirmationDialog
//         open={Boolean(confirmationState)}
//         onSubmit={handleSubmit}
//         onClose={handleClose}
//         {...confirmationState}
//       />
//     </>
//   );
// };
