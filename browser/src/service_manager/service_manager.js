import APIService from '@/services/api_service';

const ServiceManagerUrl = 'http://localhost:2354';

export default class ServiceManager {
  state = 'IDLE';

  apiService = null;

  constructor() {
    this.apiService = new APIService(ServiceManagerUrl);
  }

  // async sendStartRequest() {

  // }

  // async sendSearchText() {

  // }

  // async sendEndRequest() {

  // }

  async getServerState() {
    console.log('service-manager: getServiceState');
    const data = await this.apiService.get();
    console.log(data);
    if (data.message === 'Manager status') {
      this.state = data.state;
      // eslint-disable-next-line no-template-curly-in-string
      console.log(`data.state: ${this.state}`);
    }
  }

  get state() {
    return this.state;
  }
}
