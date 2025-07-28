from crewai.utilities.events import (
    LLMCallStartedEvent,
    LLMCallCompletedEvent
)
from crewai.utilities.events.knowledge_events import (
    KnowledgeRetrievalStartedEvent,
    KnowledgeRetrievalCompletedEvent,
    KnowledgeQueryStartedEvent,
    KnowledgeQueryCompletedEvent
)
from datetime import datetime

from crewai.utilities.events.base_event_listener import BaseEventListener
call_counter = {"count": 0}

class LlmMonitor(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
       
        @crewai_event_bus.on(LLMCallStartedEvent)
        def on_llm_call_started(source, event):
            call_counter["count"] += 1
            print("\n" + "="*80)
            print(f"🤖 LLM CALL #{call_counter['count']} STARTED at {datetime.now().strftime('%H:%M:%S')}")
            print("="*80)
            
            # Print the messages being sent to LLM
            if hasattr(event, 'messages') and event.messages:
                for i, message in enumerate(event.messages):
                    print(f"\n📝 Message {i+1}:")
                    print(f"   Role: {message.get('role', 'unknown')}")
                    content = message.get('content', 'unknown')
                    print(f"   Content: {content}")
                    print("-" * 40)
            
            # Print any additional event attributes
            print(f"\n🔍 Event Details:")
            event_attrs = ['model', 'temperature', 'max_tokens', 'agent', 'task']
            for attr in event_attrs:
                if hasattr(event, attr):
                    value = getattr(event, attr)
                    print(f"   {attr}: {value}")
            
            print("="*80)
        
        @crewai_event_bus.on(LLMCallCompletedEvent)
        def on_llm_call_completed(source, event):
            print(f"\n✅ LLM CALL #{call_counter['count']} COMPLETED")
            if hasattr(event, 'response'):
                response = str(event.response)
                print(f"   Response: {response}")
            print("-" * 40)

class KnowledgeMonitor(BaseEventListener):
    def setup_listeners(self, crewai_event_bus):
        @crewai_event_bus.on(KnowledgeRetrievalStartedEvent)
        def on_knowledge_retrieval_started(source, event):
            print(f"🔍 Agent '{event.agent.role}' started retrieving knowledge")
            
        @crewai_event_bus.on(KnowledgeRetrievalCompletedEvent)
        def on_knowledge_retrieval_completed(source, event):
            print(f"✅ Agent '{event.agent.role}' completed knowledge retrieval")
            print(f"📝 Query: {event.query}")
            print(f"📚 Retrieved {len(event.retrieved_knowledge)} knowledge chunks")
            # Optional: print first few chars of each chunk
            for i, chunk in enumerate(event.retrieved_knowledge[:3]):  # Show first 3 chunks
                print(f"  Chunk {i+1}: {str(chunk)[:100]}...")
       
        @crewai_event_bus.on(KnowledgeQueryStartedEvent)
        def on_knowledge_query_started(source, event):
            print(f"\n🔍 KNOWLEDGE QUERY STARTED")
            if hasattr(event, 'query'):
                print(f"   Query: {event.query}")
            if hasattr(event, 'agent'):
                agent_role = getattr(event.agent, 'role', 'Unknown') if event.agent else 'Unknown'
                print(f"   Agent: {agent_role}")
            if hasattr(event, 'source'):
                print(f"   Knowledge Source: {event.source}")
            print(f" KNOWLEDGE QUERY STARTED - event:{event}")
        @crewai_event_bus.on(KnowledgeQueryCompletedEvent)
        def on_knowledge_query_completed(source, event):
            print(f"\n✅ KNOWLEDGE QUERY COMPLETED")
            print (f" KNOWLEDGE QUERY COMPLETED - event:{event}")
            if hasattr(event, 'query'):
                print(f"   Query: {event.query}")
            if hasattr(event, 'results'):
                print(f"   Found {len(event.results)} results")
                for i, result in enumerate(event.results[:2]):
                    result_preview = str(result)[:150] if result else "Empty result"
                    print(f"     Result {i+1}: {result_preview}...")
            if hasattr(event, 'execution_time'):
                print(f"   Execution time: {event.execution_time}ms")
            if hasattr(event, 'agent'):
                agent_role = getattr(event.agent, 'role', 'Unknown') if event.agent else 'Unknown'
                print(f"   Agent: {agent_role}")
              