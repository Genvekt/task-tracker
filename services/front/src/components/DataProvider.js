const DataProviderBase = (server) => ({
  getList: (resource) => {
    console.log(resource);
    return server.get(resource).then((response) => response.data);
  },
  getOne: (resource, id) => {
    return server.get(`${resource}/${id}`).then((response) => response.data);
  },
  updateOne: (resource, id, data) => {
    return server
      .put(`${resource}/${id}`, data)
      .then((response) => response.data);
  },
  createOne: (resource, data) => {
    return server
      .post(resource, data)
      .then((response) => response.data)
      .catch(function (error) {
        throw error;
      });
  },
});

export const DataProvider = (server) => ({
  ...DataProviderBase(server),
});
