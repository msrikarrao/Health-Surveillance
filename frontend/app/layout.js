import './globals.css'

export const metadata = {
  title: 'Health Surveillance System',
  description: 'Smart Health Surveillance and Early Warning System',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
