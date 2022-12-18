import authHeader from "@/services/authHeader";

const DataProviderBase = (server) => ({
  getList: (resource) => {
    console.log(resource);
    return server
      .get(resource, { headers: authHeader() })
      .then((response) => response.data);
  },
  getOne: (resource, id) => {
    return server
      .get(`${resource}/${id}`, { headers: authHeader() })
      .then((response) => response.data);
  },
  updateOne: (resource, id, data) => {
    return server
      .put(`${resource}/${id}`, data, { headers: authHeader() })
      .then((response) => response.data);
  },
  createOne: (resource, data) => {
    return server
      .post(resource, data, { headers: authHeader() })
      .then((response) => response.data)
      .catch(function (error) {
        throw error;
      });
  },
});

export const DataProvider = (server) => ({
  ...DataProviderBase(server),
});
