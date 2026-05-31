import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"

type AuthFormProps = {
  title: string
  username: string
  password: string
  setUsername: (value: string) => void
  setPassword: (value: string) => void
  handleSubmit: () => void
  buttonText: string

  footerText: string
  footerLinkText: string
  footerLinkTo: string
}

function AuthForm({
  title,
  username,
  password,
  setUsername,
  setPassword,
  handleSubmit,
  buttonText,
  footerText,
  footerLinkText,
  footerLinkTo
}: AuthFormProps) {
  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center px-4">

      <Card className="w-full max-w-md bg-zinc-900 border-zinc-800 text-white">

        <CardHeader>
          <CardTitle className="text-3xl text-center">
            {title}
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-5">

          <Input
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="bg-zinc-800 border-zinc-700"
          />

          <Input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-zinc-800 border-zinc-700"
          />

          <Button
            onClick={handleSubmit}
            className="w-full"
          >
            {buttonText}
          </Button>

        </CardContent>

        <div className="mt-4 text-center text-sm text-zinc-400">

          {footerText}{" "}
            <Link  to={footerLinkTo}  className="text-white hover:underline" >
              {footerLinkText}
            </Link>

        </div>
      </Card>

    </div>
  )
}

export default AuthForm