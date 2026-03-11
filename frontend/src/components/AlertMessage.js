import {Alert, AlertDescription, AlertTitle} from "@/components/ui/alert"
import {AlertCircleIcon} from "lucide-react"

export function AlertMessage({title, message}) {
    return (
        <Alert variant="destructive" className="fixed top-6 left-1/2 -translate-x-1/2 z-50 max-w-md shadow-lg">
            <AlertCircleIcon/>
            <AlertTitle>{title}</AlertTitle>
            <AlertDescription>
                {message}
            </AlertDescription>
        </Alert>
    )
}
