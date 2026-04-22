import ActionItemsTable from "./ActionItemsTable";
import DecisionsList from "./DecisionsList";
import BlockersList from "./BlockersList";
import EmailDraftView from "./EmailDraftView";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

const ResultView = ({ meeting }) => {
  if (!meeting) return null;

  return (
    <div className="space-y-10 animate-in fade-in duration-500">
      {/* 1. Executive Summary Highlight */}
      <Card className="bg-blue-50/50 border-blue-200 shadow-sm overflow-hidden">
        <div className="bg-blue-600 h-1 w-full" />
        <CardContent className="pt-6">
          <div className="flex items-center gap-2 mb-3">
            <Badge variant="outline" className="bg-blue-100 text-blue-700 border-blue-300 uppercase tracking-tighter text-[10px]">
              AI Generated Summary
            </Badge>
          </div>
          <h3 className="text-xl font-bold text-blue-900 mb-2">Executive Summary</h3>
          <p className="text-blue-800 leading-relaxed italic text-lg">
            "{meeting.short_summary}"
          </p>
        </CardContent>
      </Card>

      {/* 2. Detailed Summary Section */}
      <section className="space-y-4">
        <div className="flex items-center gap-2">
          <h2 className="text-2xl font-bold tracking-tight">Detailed Overview</h2>
        </div>
        <Separator />
        <Card className="border-none shadow-none bg-transparent">
          <CardContent className="p-0">
            <p className="text-gray-700 leading-7 whitespace-pre-wrap">
              {meeting.detailed_summary}
            </p>
          </CardContent>
        </Card>
      </section>

      {/* 3. Core Outcomes Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        <div className="space-y-2">
          <ActionItemsTable items={meeting.action_items || []} />
        </div>
        <div className="space-y-2">
          <DecisionsList items={meeting.decisions || []} />
        </div>
      </div>

      {/* 4. Blockers and Risks */}
      <section className="space-y-4">
         <BlockersList items={meeting.blockers || []} />
      </section>

      {/* 5. Follow-up Assets */}
      <section className="pt-6">
        <EmailDraftView text={meeting.followup_email} />
      </section>
      
      <footer className="text-center pb-10">
        <p className="text-xs text-muted-foreground">
          Meeting analyzed on {new Date(meeting.created_at).toLocaleString()}
        </p>
      </footer>
    </div>
  );
};

export default ResultView;