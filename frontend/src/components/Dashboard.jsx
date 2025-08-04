import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  UsersIcon, 
  UserPlusIcon, 
  CalendarIcon, 
  CurrencyDollarIcon,
  ClipboardIcon,
  CubeIcon,
  DocumentTextIcon,
  ChatBubbleLeftIcon,
  ArrowRightOnRectangleIcon
} from '@heroicons/react/24/outline';

function Dashboard({ user, onLogout }) {
  const navigate = useNavigate();

  const menuItems = [
    {
      title: 'Patients',
      description: 'Manage patient records',
      icon: UsersIcon,
      path: '/patients',
      color: 'bg-blue-500'
    },
    {
      title: 'Doctors',
      description: 'Doctor management',
      icon: UserPlusIcon,
      path: '/doctors',
      color: 'bg-green-500'
    },
    {
      title: 'Appointments',
      description: 'Schedule & view appointments',
      icon: CalendarIcon,
      path: '/appointments',
      color: 'bg-purple-500'
    },
    {
      title: 'Billing',
      description: 'Billing & payments',
      icon: CurrencyDollarIcon,
      path: '/billing',
      color: 'bg-yellow-500'
    },
    {
      title: 'Staff',
      description: 'Staff management',
      icon: ClipboardIcon,
      path: '/staff',
      color: 'bg-indigo-500'
    },
    {
      title: 'Inventory',
      description: 'Medical inventory',
      icon: CubeIcon,
      path: '/inventory',
      color: 'bg-red-500'
    },
    {
      title: 'Medical Records',
      description: 'Patient medical records',
      icon: DocumentTextIcon,
      path: '/medical-records',
      color: 'bg-teal-500'
    },
    {
      title: 'Feedback',
      description: 'Patient feedback',
      icon: ChatBubbleLeftIcon,
      path: '/feedback',
      color: 'bg-pink-500'
    }
  ];

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    onLogout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">JK HOSPITALS</h1>
              <p className="text-sm text-gray-600">Hospital Management System</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Welcome, {user?.username}</span>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-gray-500 hover:text-gray-700"
              >
                <ArrowRightOnRectangleIcon className="h-5 w-5" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h2>
          <p className="text-gray-600">Manage your hospital operations efficiently</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UsersIcon className="h-8 w-8 text-blue-500" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-semibold text-gray-900">--</p>
                <p className="text-gray-600">Total Patients</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <UserPlusIcon className="h-8 w-8 text-green-500" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-semibold text-gray-900">--</p>
                <p className="text-gray-600">Total Doctors</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CalendarIcon className="h-8 w-8 text-purple-500" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-semibold text-gray-900">--</p>
                <p className="text-gray-600">Appointments Today</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ClipboardIcon className="h-8 w-8 text-indigo-500" />
              </div>
              <div className="ml-4">
                <p className="text-2xl font-semibold text-gray-900">--</p>
                <p className="text-gray-600">Total Staff</p>
              </div>
            </div>
          </div>
        </div>

        {/* Menu Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {menuItems.map((item, index) => (
            <button
              key={index}
              onClick={() => navigate(item.path)}
              className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6 text-left group"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`${item.color} p-3 rounded-lg`}>
                  <item.icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2 group-hover:text-blue-600">
                {item.title}
              </h3>
              <p className="text-gray-600 text-sm">{item.description}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;