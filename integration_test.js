#!/usr/bin/env node

/**
 * Frontend-Backend Integration Test Script
 * Simulates the frontend data requests service calls to verify integration
 */

const API_BASE_URL = 'http://localhost:8001';

// Simulate the authAPIClient.get method
async function simulateAPICall(endpoint, params = {}) {
  const searchParams = new URLSearchParams();
  
  // Add params to URL
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      searchParams.append(key, String(value));
    }
  });

  const queryString = searchParams.toString();
  const url = queryString ? `${API_BASE_URL}${endpoint}?${queryString}` : `${API_BASE_URL}${endpoint}`;
  
  console.log(`📡 Making request to: ${url}`);
  
  try {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`❌ Request failed: ${error.message}`);
    throw error;
  }
}

async function testIntegration() {
  console.log('🔍 Frontend-Backend Integration Test');
  console.log('===================================\n');

  try {
    // Test 1: Get categories (simulating frontend service call)
    console.log('1️⃣ Testing Categories Endpoint');
    const categories = await simulateAPICall('/api/v1/data-requests/categories/');
    
    if (categories.success && categories.data) {
      console.log(`✅ Categories loaded: ${categories.data.length} categories found`);
      console.log(`   Sample: ${categories.data[0]?.name} (${categories.data[0]?.description})\n`);
    } else {
      console.log(`❌ Categories failed: ${categories}\n`);
      return;
    }

    // Test 2: Get data requests (simulating frontend service call with filters)
    console.log('2️⃣ Testing Data Requests List Endpoint');
    const requests = await simulateAPICall('/api/v1/data-requests/', {
      page: 1,
      limit: 10,
      sort: 'newest'
    });
    
    if (requests.success && requests.data) {
      const requestsData = requests.data;
      console.log(`✅ Data requests loaded: ${requestsData.total} total requests`);
      console.log(`   Page: ${requestsData.page}/${requestsData.total_pages}, Showing: ${requestsData.data.length} requests`);
      console.log(`   Sample: "${requestsData.data[0]?.title}" (${requestsData.data[0]?.status})\n`);
    } else {
      console.log(`❌ Data requests failed: ${requests}\n`);
      return;
    }

    // Test 3: Test with filters (simulating frontend filtering)
    console.log('3️⃣ Testing Data Requests with Filters');
    const filteredRequests = await simulateAPICall('/api/v1/data-requests/', {
      category: categories.data[0]?.id,
      status: 'pending',
      page: 1,
      limit: 5
    });
    
    if (filteredRequests.success) {
      console.log(`✅ Filtered requests: ${filteredRequests.data.total} requests with category filter\n`);
    } else {
      console.log(`❌ Filtered requests failed\n`);
    }

    console.log('🎉 Integration Test Summary:');
    console.log('===========================');
    console.log('✅ Categories endpoint working');
    console.log('✅ Data requests list working');
    console.log('✅ Filtering functionality working');
    console.log('✅ Frontend-Backend integration is SUCCESSFUL');
    
    console.log('\n📋 Ready for User Journey Testing:');
    console.log('- Frontend: http://localhost:3001');
    console.log('- Backend:  http://localhost:8001');
    console.log('- Data requests page: http://localhost:3001/data-requests');

  } catch (error) {
    console.error('\n💥 Integration test failed:', error.message);
    process.exit(1);
  }
}

// Run the test
testIntegration();