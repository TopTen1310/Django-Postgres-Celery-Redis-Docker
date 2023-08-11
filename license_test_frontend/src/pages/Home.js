import { useEffect, useState, useMemo, useCallback } from 'react'
import Table from '../components/Table'
import { Button } from '../components/Button'
import { NotificationManager } from 'react-notifications'
import { ApiService } from '../lib/apis'

const Home = () => {
  // State variables for Home
  const [notiHistory, setNotiHistory] = useState([])

  // Hooks for Home
  const columns = useMemo(
    () => [
      {
        Header: 'Client Name',
        accessor: 'client_name',
      },
      {
        Header: 'Expiring license count',
        accessor: 'expiring_license_count',
      },
      {
        Header: 'Client POC Contact Name',
        accessor: 'poc_contact_name',
      },
      {
        Header: 'Client POC Email',
        accessor: 'poc_contact_email',
      },
      {
        Header: 'Admin POC Email',
        accessor: 'admin_poc_email',
      },
      {
        Header: 'Date of Notification',
        accessor: 'created',
      },
    ],
    [],
  )

  // Callbacks for Home
  const handleTrigger = useCallback(() => {
    ApiService(`/api/license/`, 'POST').then((data) => {
        setNotiHistory(
          data.notifications.map((item) => ({
            ...item,
            ...item.client,
          })),
        )
        NotificationManager.info(
          'Info',
          `${data.triggered_notifications} notifications triggered!`,
        )
      })
    NotificationManager.success('Success', 'Trigger sent!')
  }, [])

  // useEffects for Home
  useEffect(() => {
    ApiService(`/api/license/`)
      .then((data) =>
        setNotiHistory(
          data.map((item) => ({
            ...item,
            ...item.client,
          })),
        ),
      )
      .catch((err) => {
        console.log('Failed to fetch data from server\n', err)
        NotificationManager.error('Error', 'Notifications Fetched failed')
      })
    NotificationManager.success('Success', 'Notifications Fetched successfully')
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <main className="max-w-5xxl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
        <div className="flex justify-between">
          <h1 className="text-xl font-semibold">
            Frontend for Castlabs Django Test Project
          </h1>
          <Button onClick={handleTrigger}>Trigger</Button>
        </div>
        <div className="mt-6">
          <Table columns={columns} data={notiHistory} />
        </div>
      </main>
    </div>
  )
}

export default Home
