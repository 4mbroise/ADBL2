import axios from 'axios';
require('dotenv').config()

const API_BASE_URL = process.env['NEXT_PUBLIC_API_BASE_URL'] //'http://192.168.237.233:10250'; // Replace with your API base URL


const apiService = axios.create({
  baseURL: API_BASE_URL,
});

export const fetchModels = async () => {
  try {
    const response = await apiService.get('/models');
    return response.data;
  } catch (error) {
    throw error;
  }
};

export const predictBinRelation = async (model, topArgument, subArgument, promptTechnique) => {
  try {
    const response = await apiService.post('/predict', {
      model: model,
      topArgument: topArgument,
      subArgument: subArgument,
      promptTechnique: promptTechnique
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};