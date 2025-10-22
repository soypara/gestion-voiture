export const registerUser = (data) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ status: 201, data: { message: "Utilisateur créé !" } });
    }, 500);
  });
};
