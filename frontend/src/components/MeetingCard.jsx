import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useNavigate } from "react-router-dom";

const MeetingCard = ({ meeting }) => {
  const navigate = useNavigate();

  return (
    <Card 
      className="cursor-pointer hover:border-blue-400 transition-all"
      onClick={() => navigate(`/meeting/${meeting.id}`)}
    >
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-lg font-bold">{meeting.title}</CardTitle>
        <Badge variant={meeting.status === 'completed' ? 'default' : 'secondary'}>
          {meeting.status}
        </Badge>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2">
          {meeting.short_summary || "No summary available yet."}
        </p>
      </CardContent>
      <CardFooter className="flex gap-4 text-[10px] text-gray-400 uppercase tracking-wider">
        <span>📅 {meeting.meeting_date}</span>
        <span>✅ {meeting.action_item_count || 0} Actions</span>
      </CardFooter>
    </Card>
  );
};

export default MeetingCard;