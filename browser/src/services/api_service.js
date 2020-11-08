import axios from 'axios';

export default class APIService {
  API_URL = '';

  constructor(apiAddress) {
    this.API_URL = apiAddress;
  }

  async get() {
    console.log('ApiService: get()');
    try {
      const response = await axios.get(this.API_URL);
      console.log(`ApiService: get result: ${response.data}`);
      return response.data;
    } catch (error) {
      console.error(error);
      return error;
    }
  }

  async postPlainText(data) {
    console.log(`ApiService: post() - data: ${data}`);
    try {
      const response = await axios.post(this.API_URL,
        data,
        {
          headers: {
            'Content-Type': 'text/plain',
            Accept: '*/*',
          },
        });
      console.log(`ApiService: get result: ${response.data}`);
      return response.data;
    } catch (error) {
      console.error(error);
      return error;
    }
  }
}
